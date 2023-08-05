"""Exposes fastz under a nicer name."""
import fastz
import numpy as np
from fastz import *

__all__ = [
    'fastz',
    'R',
    'Rv'
    'C',
    'L',
    'Z',
    'SeriesZ',
    'ParallelZ',
    'LumpedElement',
]


class Rv(R):
    """Virtual AC input resistance of a TIA."""

    @property
    def prefix(self):
        return 'Rv'

    def __call__(self, ff, **lumpedparam):
        return np.asarray(ff) * self._lookup_value(**lumpedparam)
