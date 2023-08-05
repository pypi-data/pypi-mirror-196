"""Spectrometer driver for time tags using Swabian Instruments."""
import os
import pathlib
import sys
import warnings
from typing import Any, Dict, Iterator, Optional, Union, Sequence, Tuple, Callable

from qutil.measurement.spectrometer.daq.settings import DAQSettings

try:
    from numpy.typing import NDArray
except ImportError:
    from numpy import ndarray as NDArray


def timetagger(tagger: 'TimeTagger.TimeTagger',
               channel: Union[int, Sequence[int]] = 1,
               driver_path: Optional[Union[str, os.PathLike]] = None) -> Tuple[Callable, Callable]:
    """Generates setup and acquisition functions for a Swabian
    Instruments TimeTagger.

    This uses the Counter object to create a stream of photon numbers.

    See :class:`~qutil.measurement.spectrometer.core.Spectrometer` for
    more details on usage and
    :class:`~qutil.measurement.spectrometer.daq.settings.DAQSettings`
    for more information on setup parameters.

    Parameters
    ----------
    tagger : TimeTagger.TimeTagger
        The ``TimeTagger`` instance representing the hardware device.
    channel : int or sequence of ints
        The channel(s) to read out. The counts of all channels are
        accumulated before they are returned.
    driver_path : str | os.PathLike
        The path to the ``TimeTagger.py`` module wrapping the C++ driver
        of the device.

    Returns
    -------
    setup, acquire : Callable

    Examples
    --------
    Use the rms-normalized output of a TimeTagger tag stream as 
    time-series data::

        import atexit, sys, numpy as np
        from qutil.measurement.spectrometer import daq, Spectrometer

        sys.path.append('C:/Program Files/Swabian Instruments/Time Tagger/driver/python')

        import TimeTagger
        tagger = TimeTagger.createTimeTagger()
        tagger.setTriggerLevel(1, 1)  # APDs recommend 1 V
        tagger.setTriggerLevel(2, 1)
        _ = atexit.register(TimeTagger.freeTimeTagger, tagger)


        def rms_normalize(x, *_, **__):
            if np.issubdtype(x.dtype, int):
                y = x.astype('int64')  # prevent overflow
            else:
                y = x
            return x / np.sqrt((y ** 2).sum(axis=-1) / x.size)


        spect = Spectrometer(*daq.swabian_instruments.timetagger(tagger, [1, 2]),
                             procfn=rms_normalize, raw_unit='cts', processed_unit='a.u.')

    """
    driver_path = driver_path or pathlib.Path('C:/Program Files/Swabian Instruments/Time Tagger',
                                              'driver/python')
    try:
        import TimeTagger
    except ImportError:
        sys.path.append(str(driver_path))
        try:
            import TimeTagger
        except ImportError as err:
            raise ImportError('This DAQ requires the TimeTagger module which was not found at '
                              f'{driver_path}') from err

    channel = [channel] if not isinstance(channel, Sequence) else list(channel)
    assert len(channel) > 0, 'channel should be sequence of ints'
    assert all(ch > 0 for ch in channel), 'channel indexing starts at 1'

    def setup(fs: float, **settings) -> Dict[str, Any]:
        """Sets up a Keysight DMM to acquire a timetrace for given parameters."""
        # OOO structure of TimeTagger doesn't allow configuration before
        # all parameters are known, so all we can do is check if params
        # are valid.
        requested_settings = DAQSettings(fs=fs, **settings)
        actual_settings = DAQSettings(fs=fs, **settings)

        # TimeTagger uses units picoseconds
        actual_settings.fs = 1e12 / int(1e12 / requested_settings.fs)
        return DAQSettings(actual_settings).to_consistent_dict()

    def acquire(*, fs: float, n_pts: int, n_avg: int, **_) -> Iterator[NDArray]:
        """Executes a measurement and yields the resulting timetrace."""
        duration = int(1e12 / fs) * n_pts
        counter = TimeTagger.Counter(tagger, channel, duration / n_pts, n_pts)

        for _ in range(n_avg):
            counter.startFor(duration, clear=True)
            counter.waitUntilFinished(2 * duration)

            data = counter.getDataObject()
            if (mask := data.getOverflowMask()).any():
                warnings.warn(f'Data overflow detected in {mask.sum()} bins', RuntimeWarning)
            if data.dropped_bins:
                warnings.warn(f'{data.dropped_bins} dropped bins detected', RuntimeWarning)
            yield data.getData().sum(axis=0)

        return counter.getConfiguration()

    return setup, acquire
