r"""Spectrometer drivers for Zurich Instruments devices.

Currently implemented are drivers for the DAQ and the scope module of
the MFLI.

Examples
--------
Start up a session and connect the device::

    from zhinst import toolkit

    session = toolkit.Session('localhost')
    device = session.connect_device('dev5247', interface='1gbe')

Set up :class:`~qutil.measurement.spectrometer.Spectrometer` instances
once using the DAQ module and once using the Scope module::

    import tempfile
    from qutil.measurement.spectrometer import Spectrometer
    from qutil.measurement.spectrometer.daq import zhinst

    savepath = tempfile.TemporaryDirectory().name
    spect_daq = Spectrometer(*zhinst.MFLI_daq(session, device),
                             plot_absolute_frequencies=False,
                             savepath=savepath)
    spect_scope = Spectrometer(*zhinst.MFLI_scope(session, device),
                               savepath=savepath)

Compare their results::

    spect_daq.take(n_pts=2**14, fs=14.6e3, freq=500)
    spect_scope.take(n_pts=2**14, fs=14.6e3)

The DAQ spectrum should show a peak at :math:`f=-500\,\mathrm{Hz}`,
corresponding to the oscillator frequency.

"""
import logging
import time
from typing import Optional, Union, Mapping, Iterator, Tuple

import numpy as np
from packaging import version
from scipy.special import gamma

from qutil.measurement.spectrometer.daq.settings import DAQSettings
from qutil.misc import filter_warnings

try:
    from numpy.typing import ArrayLike
except ImportError:
    from numpy import ndarray as ArrayLike

try:
    from zhinst import toolkit, utils
    from zhinst.core.errors import SampleLossError
    if version.parse(toolkit.__version__) < version.parse('0.5.0'):
        raise ImportError('This driver requires zhinst.toolkit >= 0.5.0')
except ImportError:
    from unittest import mock

    utils = None
    toolkit = mock.Mock()

logger = logging.getLogger(__name__)


def MFLI_daq(session: toolkit.session.Session,
             device: Union[str, toolkit.driver.devices.base.BaseInstrument],
             demod: int = 0, osc: int = 0) -> Tuple[callable, callable]:
    """Use the DAQ module to acquire spectra of demodulated data.

    The data returned is a complex sum of in-phase and quadrature
    components, X + iY, and therefore the resulting spectrum is two-
    sided.

    .. note::

        For measurements where the input is not connected to the output
        of the Lock-in, this means there is a coherent signal at the
        oscillator frequency present in the time series data. Due to
        non-idealities, its peak in the spectrum has a finite width and
        may thus overshadow spectral features present in the input.

    Parameters
    ----------
    session : toolkit.session.Session
        A zhinst session to manage devices.
    device : Union[str, toolkit.driver.devices.base.BaseInstrument]
        Either a serial string, e.g., 'dev5247', or a toolkit device
        object representing the MFLI.
    demod : int, optional
        The demodulator to use. The default is 0.
    osc : int, optional
        The oscillator to use. The default is 0.

    Returns
    -------
    setup, acquire : Callable

    See Also
    --------
    :func:`MFLI_scope` :
        Acquisition using the scope module, meaning data is acquired
        directly from the device's ADC (before being demodulated).

    """
    if utils is None:
        raise ImportError('This DAQ requires zhinst-toolkit. You can install it by running '
                          "'pip install zhinst-toolkit'.")

    with filter_warnings('error'):
        utils.api_server_version_check(session.daq_server)

    if isinstance(device, str):
        device = session.connect_device(device)

    device.check_compatibility()

    assert 'LI' in device.device_type

    daq_module = session.modules.daq
    daq_module.device(device)

    # While it might look like one could just subscribe to the node string, this will fail
    # silently, so we must subscribe to the actual node
    sample_nodes = [
        device.demods[demod].sample.x,
        device.demods[demod].sample.y
    ]

    CLOCKBASE = device.clockbase()
    # TODO: always the same for each instrument?
    ALLOWED_SAMPLE_RATES = CLOCKBASE / 70 / 2**np.arange(24)

    def setup(bandwidth: Union[str, float] = 'auto', filter_order: Optional[int] = None,
              freq: float = 0, **settings: Mapping):
        r"""Sets up the daq module to acquire time series data.

        See [1]_ for information on lock-in measurements.

        Parameters
        ----------
        bandwidth : Union[str, float], optional
            The demodulator noise-equivalent power (NEP) bandwidth.
            The default is 'auto', in which case it is set to f_max/2.

            The bandwidth is related to the time constant of the RC
            filter by

            .. math::

                \tau = \frac{\Gamma\left(n - \frac{1}{2}\right)}
                            {4\sqrt{\pi}f_\mathrm{NEP}\Gamma(n)},

            where :math:`n` is the filter order

        filter_order : int, optional
            The filter order. Not changed if not given.
        freq : float, optional
            The demodulation (local oscillator) frequency. The default
            is 0. You can control if physical frequencies or
            downconverted frequencies are plotted in the spectrometer
            by setting
            :attr:`~qutil.measurement.spectrometer.Spectrometer.plot_absolute_frequencies`.

            .. note::

                Other frequency settings such as ``f_max`` will be
                referenced to ``freq``, meaning for instance if
                ``freq = 10e3, f_max = 2e3``, the spectrum will have a
                bandwidth of ``[8e3, 12e3]``.
        **settings : Mapping
            Additional settings for data acqusition.

        Raises
        ------
        RuntimeError
            If settings are incompatible with the hardware.

        Returns
        -------
        settings : dict
            A consistent set of DAQ settings.

        References
        ----------
        .. [1] https://www.zhinst.com/europe/en/resources/principles-of-lock-in-detection

        """
        requested_settings = DAQSettings(freq=freq, **settings)
        actual_settings = DAQSettings(freq=freq, **settings)

        # Round fs to next-largest allowed value
        fs = ALLOWED_SAMPLE_RATES[ALLOWED_SAMPLE_RATES >= requested_settings.fs][-1]

        if bandwidth == 'auto':
            bandwidth = requested_settings.f_max / 2

        if filter_order:
            device.demods[demod].order(int(filter_order))

        # BW 3dB = √(2^(1/n) - 1) / 2πτ
        # BW NEP = Γ(n - 1/2) / 4τ √(π)Γ(n)
        n = device.demods[demod].order()
        tc = gamma(n - 0.5) / (4 * bandwidth * np.sqrt(np.pi) * gamma(n))

        # Do not use context manager here because somehow settings can get lost
        # with device.set_transaction():
        device.oscs[osc].freq(freq)
        device.demods[demod].rate(fs)
        device.demods[demod].timeconstant(tc)

        # Update settings with device parameters. Do this before evaluating settings.n_pts below,
        # otherwise fs is constrained.
        actual_settings['bandwidth'] = (
            gamma(n - 0.5) / (4 * device.demods[demod].timeconstant() * np.sqrt(np.pi) * gamma(n))
        )
        actual_settings['filter_order'] = n
        try:
            actual_settings.fs = fs
        except ValueError as error:
            raise RuntimeError(f'Hardware constrains fs to {fs}, which is incompatible with '
                               'other settings and this code is too dumb to be smart about '
                               'this.') from error

        assert np.allclose(fs, device.demods[demod].rate())

        daq_module.type(0)  # continuous acquisition (trigger off)
        daq_module.endless(1)  # continous triggering
        daq_module.bandwidth(0)  # no filter on trigger signal

        daq_module.grid.mode(4)  # 4: exact, 2: linear interpolation
        daq_module.grid.direction(0)  # forward
        daq_module.grid.overwrite(0)  # multiple data chunks returned
        daq_module.grid.waterfall(0)  # data from newest trigger event always in row 0
        daq_module.grid.rowrepetition(1)  # row-wise repetition off
        daq_module.grid.rows(1)  # number of rows in the grid (we use count for outer repetitions)
        daq_module.grid.cols(actual_settings.n_pts)  # number of points per row

        daq_module.unsubscribe('*')
        for node in sample_nodes:
            daq_module.subscribe(node)

        return actual_settings.to_consistent_dict()

    def acquire(*, n_avg: int, **_) -> Iterator[ArrayLike]:
        """Executes a measurement and yields the resulting timetrace."""
        # Set the number of outer averages
        # daq_module.grid.rows(n_avg)
        daq_module.count(n_avg)  # number of grids to acquire
        # Clear all data from server for good measure
        daq_module.finish()
        daq_module.read()
        # Enable data transfer
        device.demods[demod].enable(1)

        # make sure we're ready
        session.sync()
        # arm the acquisition
        daq_module.execute()

        # Stupid wait because daq_module.duration() needs a while before it
        # returns the correct value
        time.sleep(1)

        trigger_timeout = max(1.5 * daq_module.duration(), 2)
        trigger_start = time.time()
        while (trigger_time := time.time() - trigger_start) < trigger_timeout:
            data = daq_module.read(raw=False, clk_rate=CLOCKBASE)
            if '/triggered' in data and data['/triggered'][0] == 1:
                break
        else:
            raise TimeoutError('Timeout during wait for trigger')
        logger.info(f'Trigger time was {trigger_time}.')

        acquisition_timeout = max(1.5 * daq_module.duration(), 2)
        yielded_records = 0
        data = []
        for record in range(n_avg):
            acquisition_start = time.time()
            while len(data) <= yielded_records:
                if (acquisition_time := (time.time() - acquisition_start)) > acquisition_timeout:
                    raise TimeoutError(f'Timeout during acquisition of record {record}')
                if new_data := daq_module.read(raw=True, clk_rate=CLOCKBASE):
                    # convert dict of list to list of dicts to be compatible with Spectrometer
                    new_records = len(new_data[sample_nodes[0]])
                    for rec in range(new_records):
                        data.append({str(node): new_data[node][rec] for node in sample_nodes})
                        if any(not np.isfinite(d['value']).all() for d in data[-1].values()):
                            raise SampleLossError('Detected non-finite values in record '
                                                  f'{len(data)}')

                    logger.info(f'Fetched {new_records} new records.')
                    logger.info(f'Acquisition time for records {record}--{record + new_records} '
                                f'was {acquisition_time}.')

            logger.info(f'Yielding record {record}.')
            yielded_records += 1
            yield sum(data[record][str(node)].pop('value').squeeze() * unit
                      for unit, node in zip([1, 1j], sample_nodes))

        # Clean up
        daq_module.finish()
        # Return all metadata that was acquired
        return data[:n_avg]

    return setup, acquire


def MFLI_scope(session: toolkit.session.Session,
               device: Union[str, toolkit.driver.devices.base.BaseInstrument],
               scope: int = 0) -> Tuple[callable, callable]:
    """Use the Scope module to acquire spectra of ADC data.

    .. note::

        The scope module can only acquire 16384 samples at a time. If
        you need a higher resolution, use the DAQ module.

    Parameters
    ----------
    session : toolkit.session.Session
        A zhinst session to manage devices.
    device : Union[str, toolkit.driver.devices.base.BaseInstrument]
        Either a serial string, e.g., 'dev5247', or a toolkit device
        object representing the MFLI.
    scope : int, optional
        The scope channel to use. The default is 0.

    Returns
    -------
    setup, acquire : Callable

    See Also
    --------
    :func:`MFLI_daq` :
        Acquisition using the DAQ module, meaning data is acquired
        after it has been demodulated.

    """

    if utils is None:
        raise ImportError('This DAQ requires zhinst-toolkit. You can install it by running '
                          "'pip install zhinst-toolkit'.")

    with filter_warnings('error'):
        utils.api_server_version_check(session.daq_server)

    if isinstance(device, str):
        device = session.connect_device(device)

    device.check_compatibility()

    assert 'LI' in device.device_type

    CLOCKBASE = device.clockbase()
    ALLOWED_SAMPLE_RATES = CLOCKBASE / 2**np.arange(17)
    scope_module = session.modules.scope

    def check_scope_record_flags(scope_records):
        """
        Loop over all records and print a warning to the console if an error bit in
        flags has been set.

        From https://docs.zhinst.com/zhinst-toolkit/en/latest/examples/scope_module.html
        """
        num_records = len(scope_records)
        for index, record in enumerate(scope_records):
            record_idx = f"{index}/{num_records}"
            record_flags = record[0]["flags"]
            logger.debug(f'Record {index} has flags {record_flags}.')
            if record_flags & 1:
                print(f"Warning: Scope record {record_idx} flag indicates dataloss.")
            if record_flags & 2:
                print(f"Warning: Scope record {record_idx} indicates missed trigger.")
            if record_flags & 4:
                print(f"Warning: Scope record {record_idx} indicates transfer failure"
                      "(corrupt data).")

            totalsamples = record[0]["totalsamples"]
            for wave in record[0]["wave"]:
                # Check that the wave in each scope channel contains
                # the expected number of samples.
                assert (
                    len(wave) == totalsamples
                ), f"Scope record {index}/{num_records} size does not match totalsamples."

    def setup(**settings: Mapping):
        r"""Sets up the scope module to acquire time series data.

        Raises
        ------
        RuntimeError
            If settings are incompatible with the hardware.

        Returns
        -------
        settings : dict
            A consistent set of DAQ settings.

        """
        requested_settings = DAQSettings(**settings)
        actual_settings = DAQSettings(**settings)

        # Round fs to next-largest allowed value
        fs = ALLOWED_SAMPLE_RATES[ALLOWED_SAMPLE_RATES >= requested_settings.fs][-1]

        try:
            actual_settings.fs = fs
        except ValueError as error:
            raise ValueError(f'Hardware constrains fs to {fs}, which is incompatible with '
                             'other settings and this code is too dumb to be smart about '
                             'this.') from error

        n_pts = min(requested_settings.n_pts, 2**14)

        try:
            actual_settings.n_pts = n_pts
        except ValueError as error:
            raise ValueError(f'Hardware constrains n_pts to {n_pts}, which is incompatible '
                             'with other settings and this code is too dumb to be smart about '
                             'this.') from error

        with device.set_transaction():
            device.scopes[scope].channel(0)  # only channel 1 active
            device.scopes[scope].channels[0].bwlimit(1)  # avoids aliasing
            device.scopes[scope].length(n_pts)
            device.scopes[scope].time(np.log2(CLOCKBASE / fs))  # duration = 2^n/clockbase
            device.scopes[scope].single(0)  # continuous acquisition
            device.scopes[scope].trigenable(0)
            device.scopes[scope].trigholdoff(0.050)
            device.scopes[scope].segments.enable(0)  # requires DIG option

        assert n_pts == device.scopes[0].length()
        assert fs == CLOCKBASE / 2 ** device.scopes[0].time()

        scope_module.mode(1)  # timetrace (scaled).
        scope_module.averager.weight(0)  # no internal averaging (we do this ourselves)
        scope_module.unsubscribe('*')
        scope_module.subscribe(device.scopes[scope].wave)
        return actual_settings.to_consistent_dict()

    def acquire(*, n_avg: int, **_) -> Iterator[ArrayLike]:
        """Executes a measurement and yields the resulting timetrace."""
        # Set the number of outer averages
        scope_module.historylength(1)
        # Clear all data from server for good measure
        scope_module.finish()
        scope_module.read()
        # Enable data transfer
        device.scopes[scope].enable(1)
        # make sure we're ready
        session.sync()
        # arm the acquisition
        scope_module.execute()

        duration = device.scopes[0].length() / (CLOCKBASE / 2 ** device.scopes[0].time())
        acquisition_timeout = max(1.5 * duration, 30)
        yielded_records = 0
        data = []
        for record in range(n_avg):
            acquisition_start = time.time()
            while (fetched_records := len(data)) <= yielded_records:
                if (acquisition_time := (time.time() - acquisition_start)) > acquisition_timeout:
                    raise TimeoutError(f'Timeout during acquisition of record {record}')
                if new_records := (scope_module.records() - fetched_records):
                    # new records acquired, fetch and check for errors.
                    data.extend(scope_module.read()[device.scopes[scope].wave])
                    check_scope_record_flags(data[-new_records:])

                    logger.info(f'Fetched {new_records} new records.')
                    logger.info(f'Acquisition time for records {record}--{record + new_records} '
                                f'was {acquisition_time}.')

            logger.info('Yielding record {record}.')
            yielded_records += 1
            yield data[record][scope].pop('wave').squeeze()

        # Clean up
        scope_module.finish()
        # Return all metadata that was acquired
        return data[:n_avg]

    return setup, acquire
