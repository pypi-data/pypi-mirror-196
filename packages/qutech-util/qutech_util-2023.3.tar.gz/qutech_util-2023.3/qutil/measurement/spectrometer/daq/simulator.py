"""Provides a simulation backend for data acquisition."""
from typing import Any, Callable, Dict, Iterator, Optional

import numpy as np

from qutil.functools import partial
from qutil.measurement.spectrometer.daq.settings import DAQSettings

try:
    from numpy.typing import NDArray
except ImportError:
    NDArray = np.ndarray


def qopt_colored_noise(spectral_density: Optional[Callable] = None):
    """Simulate noise using ``qopt``.

    See :class:`~qutil.measurement.spectrometer.core.Spectrometer` for
    more details on usage and
    :class:`~qutil.measurement.spectrometer.daq.settings.DAQSettings`
    for more information on setup parameters.

    Parameters
    ----------
    spectral_density : Callable, optional
        A callable with signature::

            f(ndarray, **settings) -> ndarray

        that returns the power spectral density for given frequencies.
        Defaults to white noise with scale parameter S_0.

    See Also
    --------
    ~qopt.noise.fast_colored_noise :
        For information on the simulation.

    """
    try:
        import qopt.noise
    except ImportError as error:
        raise ImportError('This simulated DAQ requires qopt. You can install it by running '
                          "'pip install qopt.'") from error

    def white_noise(f, S_0: float = 1.0, **_):
        return np.full_like(f, S_0)

    def setup(**settings) -> Dict[str, Any]:
        """Sets up a noise simulation for given parameters."""
        return DAQSettings(**settings).to_consistent_dict()

    def acquire(*, fs: float, n_pts: int, n_avg: int, **settings) -> Iterator[NDArray]:
        """Executes a measurement and yields the resulting timetrace."""
        for _ in range(n_avg):
            yield qopt.noise.fast_colored_noise(
                partial(
                    settings.get('spectral_density', spectral_density or white_noise),
                    **settings
                ),
                dt=1/fs, n_samples=n_pts, output_shape=()
            )
        # This is the place to return metadata (possibly obtained from the instrument)
        return {'qopt_version': qopt.__version__}

    return setup, acquire
