from typing import Any, Dict, Iterator

from qutil.measurement.spectrometer.daq.settings import DAQSettings

try:
    from numpy.typing import ArrayLike
except ImportError:
    from numpy import ndarray as ArrayLike

try:
    from qcodes_contrib_drivers.drivers.NationalInstruments import DAQ
except ImportError:
    from unittest import mock

    DAQ = mock.Mock()


def keysight_344xxA(dmm):
    """Generates setup and acquisition functions for a Keysight 344xxA DMM.

    See :class:`~qutil.measurement.spectrometer.core.Spectrometer` for more
    details on usage and
    :class:`~qutil.measurement.spectrometer.daq.settings.DAQSettings` for
    more information on setup parameters.

    Parameters
    ----------
    dmm : qcodes.Instrument
        The qcodes instrument representing the DMM.

    Returns
    -------
    setup, acquire : Callable

    """

    def setup(fs: float = 1/3e-4, **settings) -> Dict[str, Any]:
        """Sets up a Keysight DMM to acquire a timetrace for given parameters."""
        requested_settings = DAQSettings(fs=fs, **settings)
        actual_settings = DAQSettings(fs=fs, **settings)

        # Set the integration time (automatically selects aperture mode)
        dmm.aperture_time(1 / requested_settings.fs)
        # The integration time is a lower bound on the sample timer, which
        # in turn determines the time step of the measurement. So we need
        # to ask the device for the minimal allowed value of the sample timer
        # compatible with the requested integration time.
        dt = max(dmm.sample.timer_minimum(), 1 / requested_settings.fs)
        # Then we set the time step which determines our maximum frequency
        dmm.timetrace_dt(dt)

        # Set number of samples to be acquired
        dmm.timetrace_npts(requested_settings.n_pts)

        try:
            # Update the sample rate given the hardware constraints
            actual_settings.fs = 1 / dt
        except ValueError as error:
            raise ValueError(f'Hardware constrains 1/fs to {dt}, which is incompatible with '
                             'settings and this code is too dumb to be smart about '
                             'this.') from error

        try:
            # Update the sample rate given the hardware constraints
            actual_settings.n_pts = dmm.timetrace_npts()
        except ValueError as error:
            raise ValueError(f'Hardware constrains n_pts to {dmm.timetrace_npts()}, which is '
                             'incompatible with other settings and this code is too dumb to be '
                             'smart about this.') from error

        return actual_settings.to_consistent_dict()

    def acquire(*, n_avg: int, **_) -> Iterator[ArrayLike]:
        """Executes a measurement and yields the resulting timetrace."""
        for _ in range(n_avg):
            yield dmm.timetrace.get()
        return dmm.get_idn()

    return setup, acquire


def national_instruments_daq(ni_daq: DAQ.DAQAnalogInputs):
    """Generates setup and acquisition functions for a NI DAQ.

    Requires the nidaqmx package.

    See :class:`~qutil.measurement.spectrometer.Spectrometer` for more
    details on usage and :class:`~qutil.measurement.spectrometer.daq.
    settings.DAQSettings` for more information on setup parameters.

    Parameters
    ----------
    ni_daq : DAQ.DAQAnalogInputs
        The qcodes DAQAnalogInputs instrument.

    Returns
    -------
    setup, acquire : Callable

    Examples
    --------
    Use a NI DAQ to convert an analog input to a digital signal::

        from qcodes_contrib_drivers.drivers.NationalInstruments import DAQ
        import nidaqmx
        ni_daq = DAQ.DAQAnalogInputs('ni_daq', 'Dev1',
                                     rate=1, channels={0: 3},
                                     task=nidaqmx.Task(),
                                     samples_to_read=2)
        setup, acquire = national_instruments_daq(ni_daq)

    """
    try:
        import nidaqmx
    except ImportError as error:
        raise ImportError(
            'This daq requires the nidaqmx package. You can install it by running '
            "'pip install nidaqmx' and downloading the NI-DAQmx software from "
            'https://www.ni.com/en-us/support/downloads/drivers/download.ni-daqmx.htm'
        ) from error

    def setup(**settings) -> Dict[str, Any]:
        """Sets up a NI DAQ to acquire a timetrace for given parameters."""
        settings = DAQSettings(**settings)

        rate = settings.fs
        samples_to_read = settings.n_pts

        ni_daq.rate = settings.fs
        ni_daq.samples_to_read = settings.n_pts
        ni_daq.metadata.update({'rate': f'{rate} Hz'})
        ni_daq.task.timing.cfg_samp_clk_timing(
            rate,
            source=settings.get('clock_src') or '',
            sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
            samps_per_chan=samples_to_read
        )
        ni_daq.task.ai_channels[0].ai_term_cfg = settings.get(
            'terminal_configuration', nidaqmx.constants.TerminalConfiguration.DIFF
        )

        old_param = ni_daq.parameters.pop('voltage')
        ni_daq.add_parameter(
            name='voltage',
            parameter_class=DAQ.DAQAnalogInputVoltages,
            task=ni_daq.task,
            samples_to_read=samples_to_read,
            shape=(old_param.shape[0], samples_to_read),
            timeout=settings.get('timeout', old_param.timeout),
            label='Voltage',
            unit='V'
        )
        return settings.to_consistent_dict()

    def acquire(*, n_avg: int, **_) -> Iterator[ArrayLike]:
        """Executes a measurement and yields the resulting timetrace."""
        for _ in range(n_avg):
            yield ni_daq.voltage.get().squeeze()
        return ni_daq.metadata

    return setup, acquire
