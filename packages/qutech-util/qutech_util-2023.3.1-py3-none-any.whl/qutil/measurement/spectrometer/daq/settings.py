"""Provides a class that manages interdependent settings."""

import inspect
import numbers
import textwrap
from copy import copy
from math import ceil
from numbers import Real
from typing import Dict, Tuple, Union, Optional

import numpy as np

_doc_ = {
    'fs': "float.\n\tThe sampling rate. Default: ``2*f_max`` or 1e4.",
    'df': "float.\n\t" r"The frequency spacing :math:`\Delta f`. If given, supersedes ``f_min`` "
          "for computing the total duration of the record. Default: ``f_min`` or 1.0.",
    'f_max': "float.\n\tThe maximum frequency displayed. Also used for filters. Defaults to half "
             "the sample rate (fs) as per the Nyquist sampling theorem. Default: ``fs/2`` or 5e3.",
    'f_min': "float.\n\tThe smallest frequency displayed. Also used for filters. Default: ``df`` "
             "or 1.0.",
    'nperseg': "int.\n\tThe number of samples per data segment (for Welch's method). Default: "
               "``ceil(fs / df)`` or ``(npts + (nseg - 1) * noverlap) / nseg``.",
    'noverlap': "int.\n\tThe number of samples by which two adjacent segments overlap (for "
                "Welch's method). Default: ``nperseg // 2``.",
    'n_pts': "int.\n\tThe total number of samples per data buffer retrieved from a call to "
             "``acquire``. Computed by default from nperseg and noverlap.",
    'n_seg': "int.\n\tThe number of segments to average over (to be used with Welch's method). "
             "Default: 5.",
    'n_avg': "int.\n\tThe number of outer repetitions of data buffer acquisition. Data will be "
             "averaged over all repetitions. Default: 1",
}


def _nan_to_none(x: Optional[numbers.Real]) -> Optional[numbers.Real]:
    return None if np.isnan(x) else x


def _property_factory(name: str, cast_fun: callable) -> callable:
    """Automatically generate getter and setter for settings that have
    interdependencies.

    The get and set values are  coerced into the required type by
    ``cast_fun``.
    """

    def getter(self):
        return cast_fun(getattr(self, f'_{name}')())

    def setter(self, value: Real):
        old = self.get(name)
        self[name] = cast_fun(value)
        try:
            getattr(self, f'_check_{name}')(self[name])
        except ValueError:
            self[name] = old
            raise

    return getter, setter


class DAQSettings(dict):
    """A dictionary with interdependent properties.

    Parameters that can depend on the value of other parameter have
    getters and setters that are aware of those interdependencies.
    Thus, for these parameters, this should be the preferred method of
    getting and setting over dictionary-style getitem and setitem.

    To convert to a keyword-argument dictionary, use
    :meth:`to_consistent_dict`.

    The class can be used just like a regular dictionary. However,
    there are the following special, interdependent parameters
    that will be parsed for consistency upon calling
    :meth:`to_consistent_dict`.

    Parameters
    ----------
    """
    __doc__ = (
        __doc__.replace(4*' ', '')
        + '\n'.join((f'{key} : {val}' for key, val in _doc_.items()))
        + textwrap.dedent(
            """\n\n
            Examples
            --------
            There are default settings for each parameter:

            >>> DAQSettings()
            {}
            >>> DAQSettings().to_consistent_dict()  #doctest: +NORMALIZE_WHITESPACE
            {'fs': 10000.0,
             'df': 1.0,
             'f_max': 5000.0,
             'f_min': 1.0,
             'nperseg': 10000,
             'noverlap': 5000,
             'n_seg': 5,
             'n_pts': 30000,
             'n_avg': 1}

            User-settings can be passed when instantiating, and the remaining
            dependent parameters are automatically derived:

            >>> s = DAQSettings(fs=1234, n_seg=10)
            >>> s
            {'fs': 1234, 'n_seg': 10}
            >>> s.to_consistent_dict()  #doctest: +NORMALIZE_WHITESPACE
            {'fs': 1234.0,
             'n_seg': 10,
             'df': 1.0,
             'f_max': 617.0,
             'f_min': 1.0,
             'nperseg': 1234,
             'noverlap': 617,
             'n_pts': 6787,
             'n_avg': 1}

            Parameters have getters and setters. When getting, a value
            consistent with others is returned, when setting, the consistency is
            checked:

            >>> s.f_min
            1.0
            >>> s.f_min = 3
            >>> s.f_min
            3.0
            >>> s.f_max = 1000
            Traceback (most recent call last):
            ValueError: f_max > fs/2. actual = 1000.0, inferred = 617.0

            Consistency is not checked at instantiation time, only when using
            setters or converting to a plain consistent dictionary:

            >>> s = DAQSettings(nperseg=500, fs=1000, df=3)  # works
            >>> s.to_consistent_dict()  #doctest: +NORMALIZE_WHITESPACE
            Traceback (most recent call last):
            ValueError: nperseg is not compatible with {'nperseg': 500, 'fs': 1000,
            'df': 3}. See the error trace for more information.

            Test if there are no exceptions or infinite recursions for a consistent
            set of parameters (only test up to 4 keyword parameters since the
            product scales exponentially...):

            >>> import qutil.itertools
            >>> s = DAQSettings().to_consistent_dict()
            >>> for kv in qutil.itertools.product(s.items(), repeat=4):
            ...     t = DAQSettings(**dict(kv))
            ...     d = t.to_consistent_dict()
            ...     # Make sure this is reproducible
            ...     _ = DAQSettings(d).to_consistent_dict()
            ...     for k in set(s).difference(set(t)):
            ...         # use setters for remaining parameters
            ...         setattr(t, k, s[k])
            """
        )
    )

    _DEFAULTS = {
        'fs': 10e3,
        'df': 1.0,
        'n_seg': 5,
        'n_avg': 1
    }

    @property
    def _default_noverlap_mapping(self) -> Tuple[int, int]:
        """Get the default noverlap as function of nperseg.

        Returns parameters (a, b) of the linear mapping::

            nperseg = noverlap // a + b

        Can be overridden in a subclass if required.

        Returns
        -------
        (a, b) : Tuple[int, int]
            The parameters of the linear mapping.
        """
        return 2, 0

    def _check_fs(self, fs):
        inferred = self._infer_fs()
        if np.isnan(inferred):
            return
        if 'f_max' in self:
            if fs < self['f_max'] * 2:
                raise ValueError(f"fs < 2*f_max. actual = {fs}, inferred = {self['f_max'] * 2}")
            return
        if abs(fs - inferred) > 1e-12:
            raise ValueError(f'fs not compatible with df and nperseg. actual = {fs}, inferred = '
                             f'{inferred}')

    def _check_df(self, df):
        inferred = self._infer_df()
        if np.isnan(inferred):
            return
        if 'f_min' in self:
            if df > self['f_min']:
                raise ValueError(f"df > f_min. actual = {df}, inferred = {self['f_min']}")
            return
        if df != inferred:
            raise ValueError(f'df not compatible with df and nperseg. actual = {df}, inferred = '
                             f'{inferred}')

    def _check_f_max(self, f_max):
        inferred = self._infer_f_max()
        if np.isnan(inferred):
            return
        if 'fs' in self and f_max > self['fs'] / 2:
            raise ValueError(f"f_max > fs/2. actual = {f_max}, inferred = {self['fs'] / 2}")
        if f_max > inferred:
            raise ValueError(f'f_max not compatible with df and nperseg. actual = {f_max}, '
                             f'inferred = {inferred}')

    def _check_f_min(self, f_min):
        inferred = self._infer_f_min()
        if np.isnan(inferred):
            return
        if 'df' in self and f_min < self['df']:
            raise ValueError(f"f_min < df. actual = {f_min}, inferred = {self['df']}")
        if f_min < inferred:
            raise ValueError(f'f_min not compatible with fs and nperseg. actual = {f_min}, '
                             f'inferred = {inferred}')

    def _check_nperseg(self, nperseg):
        inferred = self._infer_nperseg()
        if np.isnan(inferred):
            return
        if nperseg > inferred:
            raise ValueError(f'nperseg not compatible. actual = {nperseg}, inferred = {inferred}')

    def _check_noverlap(self, noverlap):
        inferred = self._infer_noverlap()
        if np.isnan(inferred):
            return
        if 'n_pts' in self and 'n_seg' in self and noverlap != inferred:
            raise ValueError('noverlap not compatible with nperseg, n_pts, and n_seg. actual = '
                             f'{noverlap}, inferred = {inferred}')
        if 'nperseg' in self and noverlap > self['nperseg'] // 2:
            raise ValueError('unexpected')

    def _check_n_seg(self, n_seg):
        inferred = self._infer_n_seg()
        if np.isnan(inferred):
            return
        if n_seg != inferred:
            raise ValueError('n_seg not compatible with nperseg, n_pts, and noverlap. actual = '
                             f'{n_seg}, inferred = {inferred}')
        if n_seg < 1:
            raise ValueError(f'n_seg must be positive integer, not {n_seg}')

    def _check_n_pts(self, n_pts):
        inferred = self._infer_n_pts()
        if np.isnan(inferred):
            return
        if 'n_seg' in self:
            if 'noverlap' in self and n_pts != inferred:
                raise ValueError('n_pts not compatible with nperseg, n_seg, and noverlap. '
                                 f'actual = {n_pts}, inferred = {inferred}')
        if n_pts < inferred:
            raise ValueError(f'n_pts is constrained by nperseg to be >= {inferred}. '
                             f'actual = {n_pts}')
        if n_pts < 1:
            raise ValueError(f'n_pts must be positive integer, not {n_pts}')

    def _check_n_avg(self, n_avg):
        if n_avg < 1:
            raise ValueError(f'n_avg must be positive integer, not {n_avg}')

    def _infer_fs(self) -> float:
        # nan: signifies any value is allowed
        if 'df' in self:
            if 'nperseg' in self:
                nperseg = self['nperseg']
            elif 'noverlap' in self and 'n_pts' in self and 'n_seg' in self:
                if self['n_seg'] == 1:
                    nperseg = self['n_pts']
                else:
                    nperseg = int((self['n_pts'] + (self['n_seg'] - 1) * self['noverlap'])
                                  / self['n_seg'])
            else:
                nperseg = None
            if nperseg is not None:
                return self['df'] * nperseg
        if 'f_max' in self and 'fs' in self:
            return self['f_max'] * 2
        return np.nan

    def _infer_df(self) -> float:
        if 'fs' in self:
            if 'nperseg' in self:
                nperseg = self['nperseg']
            elif 'noverlap' in self and 'n_pts' in self and 'n_seg' in self:
                if self['n_seg'] == 1:
                    nperseg = self['n_pts']
                else:
                    nperseg = int((self['n_pts'] + (self['n_seg'] - 1) * self['noverlap'])
                                  / self['n_seg'])
            else:
                nperseg = None
            if nperseg is not None:
                return self['fs'] / nperseg
        if 'f_min' in self and 'df' in self:
            return self['f_min']
        return np.nan

    def _infer_f_max(self) -> float:
        if not np.isnan(fs := self.get('fs', self._infer_fs())):
            return fs / 2
        return np.nan

    def _infer_f_min(self) -> float:
        if not np.isnan(df := self.get('df', self._infer_df())):
            return df
        return np.nan

    def _infer_nperseg(self) -> Union[int, float]:
        # user-set fs or df take precedence over noverlap
        if 'fs' in self and 'df' in self:
            return int(self['fs'] / self['df'])
        a, b = self._default_noverlap_mapping
        if 'n_pts' in self:
            # cannot be larger than n_pts
            bound = self['n_pts']
            if 'n_seg' in self:
                if self['n_seg'] == 1:
                    return bound
                # noverlap is upper-bounded by nperseg // 2
                bound = min(ceil((self['n_pts'] + (self['n_seg'] - 1) * b)
                                 / (self['n_seg'] - (self['n_seg'] - 1) / a)), bound)
                if 'noverlap' in self:
                    return min(int((self['n_pts'] + (self['n_seg'] - 1) * self['noverlap'])
                                   / self['n_seg']), bound)
            return bound
        return np.nan

    def _infer_noverlap(self) -> Union[int, float]:
        if 'n_seg' in self and self['n_seg'] == 1:
            return 0
        if 'nperseg' in self:
            nperseg = self['nperseg']
        elif 'fs' in self and 'df' in self:
            nperseg = int(self['fs'] / self['df'])
        else:
            nperseg = None
        if nperseg is not None:
            bound = nperseg // 2
            if 'n_pts' in self:
                bound = min(self['n_pts'] - nperseg, bound)
                if 'n_seg' in self:
                    return min((self['n_seg'] * nperseg - self['n_pts']) // (self['n_seg'] - 1),
                               bound)
            return bound
        return np.nan

    def _infer_n_seg(self) -> Union[int, float]:
        if 'nperseg' in self:
            nperseg = self['nperseg']
        elif 'fs' in self and 'df' in self:
            nperseg = int(self['fs'] / self['df'])
        else:
            nperseg = None
        if nperseg is not None and 'n_pts' in self and 'noverlap' in self:
            return max(int((self['n_pts'] - self['noverlap']) / (nperseg - self['noverlap'])), 1)
        return np.nan

    def _infer_n_pts(self) -> Union[int, float]:
        if 'nperseg' in self:
            nperseg = self['nperseg']
        elif 'fs' in self and 'df' in self:
            nperseg = int(self['fs'] / self['df'])
        else:
            nperseg = None
        if nperseg is not None:
            # lower bounds
            bound = nperseg
            if 'n_seg' in self:
                bound = ceil((nperseg * (self['n_seg'] + 1)) / 2)
                if self['n_seg'] == 1:
                    assert bound == nperseg
                    return bound
                if 'noverlap' in self:
                    return max(int(nperseg + (self['n_seg'] - 1) * (nperseg - self['noverlap'])),
                               bound)
            return bound
        return np.nan

    def _fs(self) -> float:
        if 'fs' in self:
            return self['fs']
        if 'nperseg' in self:
            nperseg = self['nperseg']
        elif 'n_pts' in self and 'n_seg' in self and 'noverlap' in self:
            nperseg = (self['n_pts'] + (self['n_seg'] - 1) * self['noverlap']) / self['n_seg']
        else:
            nperseg = None
        if nperseg is not None:
            df = self.setdefault('df', _nan_to_none(self._infer_df()) or self._DEFAULTS['df'])
            return df * nperseg
        if 'f_max' in self:
            return self['f_max'] * 2
        return self.setdefault('fs', self._DEFAULTS['fs'])

    def _df(self) -> float:
        if 'df' in self:
            if 'fs' in self:
                # Make sure df is commensurable
                self['df'] = self['fs'] / ceil(self['fs'] / self['df'])
                if 'f_min' in self:
                    self['f_min'] = max(self['f_min'], self['df'])
            return self['df']
        if 'nperseg' in self:
            nperseg = self['nperseg']
        elif 'n_pts' in self and 'n_seg' in self and 'noverlap' in self:
            nperseg = (self['n_pts'] + (self['n_seg'] - 1) * self['noverlap']) / self['n_seg']
        else:
            nperseg = None
        if nperseg is not None:
            fs = self.setdefault('fs', _nan_to_none(self._infer_fs()) or self._DEFAULTS['fs'])
            return fs / nperseg
        if 'f_min' in self:
            return self['f_min']
        return self.setdefault('df', _nan_to_none(self._infer_df()) or self._DEFAULTS['df'])

    def _f_max(self) -> float:
        if 'f_max' in self:
            return self['f_max']
        return self.fs / 2

    def _f_min(self) -> float:
        if 'f_min' in self:
            return self['f_min']
        return self.df

    def _nperseg(self) -> int:
        if 'nperseg' in self:
            return self['nperseg']
        if not np.isnan(nperseg := self._infer_nperseg()):
            return nperseg
        # account for rounding when either fs or df have been set to a weird float and the other
        # defaults to an integer
        if 'df' not in self:
            extend_df = True
            extend_fs = False
        elif 'fs' not in self:
            extend_fs = True
            extend_df = False
        else:
            extend_fs = False
            extend_df = False
        nperseg = self.setdefault('nperseg', ceil(self.fs / self.df))
        if extend_df:
            self['df'] = self.fs / nperseg
        elif extend_fs:
            self['fs'] = self.df * nperseg
        return nperseg

    def _noverlap(self) -> int:
        if 'noverlap' in self:
            return self['noverlap']
        if not np.isnan(noverlap := self._infer_noverlap()):
            return noverlap
        a, b = self._default_noverlap_mapping
        return self.setdefault('noverlap', self.nperseg // a + b)

    def _n_seg(self) -> int:
        if 'n_seg' in self:
            return self['n_seg']
        if not np.isnan(n_seg := self._infer_n_seg()):
            return n_seg
        return self.setdefault('n_seg', self._DEFAULTS['n_seg'])

    def _n_pts(self) -> int:
        if 'n_pts' in self:
            return self['n_pts']
        if not np.isnan(n_pts := self._infer_n_pts()):
            return n_pts
        return self.setdefault('n_pts',
                               self.nperseg + (self.n_seg - 1) * (self.nperseg - self.noverlap))

    def _n_avg(self) -> int:
        return self.get('n_avg', self._DEFAULTS['n_avg'])

    # Add setters that automatically check for consistency.
    fs = property(*_property_factory('fs', float), doc=_doc_['fs'])
    df = property(*_property_factory('df', float), doc=_doc_['df'])
    f_max = property(*_property_factory('f_max', float), doc=_doc_['f_max'])
    f_min = property(*_property_factory('f_min', float), doc=_doc_['f_min'])
    nperseg = property(*_property_factory('nperseg', int), doc=_doc_['nperseg'])
    noverlap = property(*_property_factory('noverlap', int), doc=_doc_['noverlap'])
    n_seg = property(*_property_factory('n_seg', int), doc=_doc_['n_seg'])
    n_pts = property(*_property_factory('n_pts', int), doc=_doc_['n_pts'])
    n_avg = property(*_property_factory('n_avg', int), doc=_doc_['n_avg'])

    def to_consistent_dict(self) -> Dict[str, numbers.Real]:
        """Return a regular dictionary with entries checked for
        consistency."""
        # Work on a copy which we can modify at will
        copied = copy(self)
        # Make sure we parse properties that were set by the user first
        inferred_settings = {name: obj for name, obj in vars(type(copied)).items()
                             if not (name in copied or name.startswith('_'))
                             and inspect.isdatadescriptor(obj)}
        # vars(copied) are all attributes (not dict entries) that are not properties
        all_settings = {**copied, **vars(copied), **inferred_settings}

        for name, obj in all_settings.items():
            try:
                all_settings[name] = getattr(copied, name)
                getattr(copied, f'_check_{name}')(all_settings[name])
            except ValueError as e:
                raise ValueError(f'{name} is not compatible with {copied}. See the error trace '
                                 'for more information.') from e
            except AttributeError:
                pass
            # bookkeeping so that the object we use to check for consistency has all the facts
            copied[name] = all_settings[name]
        return all_settings
