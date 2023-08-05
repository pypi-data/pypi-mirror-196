"""Data acquisition drivers for the
:class:`qutil.measurement.spectrometer.Spectrometer` class.

Each submodule contains functionality for different backends, such as
QCoDeS or Zurich Instruments. A 'driver' is implemented as a function
that returns two functions itself; first, a ``setup()`` function that
configures the data acquisition device, and second, an ``acquire()``
function that when called yields an array of time-series data.
``acuire()`` can optionally return measurement metadata after the
iterator is exhausted.

More explicitly, a driver should look something like this::

    def driver(**instantiation_time_settings) -> (callable, callable):

        ...

        def setup(**configuration_settings) -> Mapping:
            ...
            return actual_device_configuration

        def acquire(n_avg: int, **runtime_settings) -> Iterator[ArrayLike]:
            ...
            for _ in range(n_avg):
                yield data
            return metadata

        return setup, acquire

The :class:`settings.DAQSettings` class provides a way of managing
interdependent settings for data acquisition, with special keywords
being reserved for parameters of the
`~qutil.signal_processing.real_space.welch` function for spectral
estimation.
"""

import lazy_loader as lazy

__getattr__, __dir__, __all__ = lazy.attach_stub(__name__, __file__)

del lazy
