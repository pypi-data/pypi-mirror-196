"""Import everything from itertools, more_itertools and some custom functions """
import warnings
from typing import Iterable, Any, Type, Tuple, Iterator

from itertools import *
from more_itertools import *


def separate_iterator(it: Iterable, sep: Any) -> Iterator:
    """separate_iterator('abcde', ',') --> a , b , c , d , e

    The same as :func:`~more_itertools.intersperse(sep, it, n=1)`. Only here for backwards compability.
    """
    warnings.warn(f"{__name__}.separate_iterator is just a wrapper around intersperse.",
                  DeprecationWarning,
                  stacklevel=2)
    return intersperse(sep, it, n=1)


def flatten_nested(it: Iterable, dtypes: Tuple[Type[Iterable], ...] = (list,)) -> Iterator:
    """Flattens the given arbitrarily nested iterable. By default, only lists are flattened. Use the optional `dtypes`
    argument to flatten other iterables as well.

    Similar to :func:`~more_itertools.collapse` which works with a blacklist instead of a whitelist.

    Parameters
    ----------
    it: :class:`~typing.Iterable` to flatten
    dtypes: Types that get flattened.

    Returns
    -------
    Objects that are not of a type in `dtypes`
    """
    if isinstance(it, dtypes):
        for x in it:
            yield from flatten_nested(x, dtypes)
    else:
        yield it


def argmax(it: Iterable) -> int:
    """Return index of largest element by iteration order.

    >>> argmax([1, 3, 2, 4, 0])
    3

    Raises
    --------
    :class:`~ValueError` if the iterable is empty.

    Parameters
    ----------
    it: :class:`~typing.Iterable` to search for maximum

    Returns
    -------
    Index of the largest element if it by iteration order
    """
    it = enumerate(it)
    try:
        max_idx, current = next(it)
    except StopIteration:
        raise ValueError('Argument was empty')
    for idx, elem in it:
        if elem > current:
            current = elem
            max_idx = idx
    return max_idx


def ignore_exceptions(it: Iterable, exceptions: Any) -> Iterator:
    """Ignore all specified exceptions during iteration.

    >>> list(filter_exceptions(map(lambda d: 5 / d, [2, 1, 0, 5]), ZeroDivisionError))
    [2.5, 5.0, 1.0]

    Be aware that some iterators do not allow further iteration if they threw an exception.
    >>> list(filter_exceptions((5 / d for d in [2, 1, 0, 5]), ZeroDivisionError))
    [2.5, 5.0]

    Parameters
    ----------
    it: :class:`~typing.Iterable` to iterate over.
    exceptions: Valid argument to an ``except`` clause
    """
    it = iter(it)
    while True:
        try:
            yield from it
        except exceptions:
            continue
        else:
            return


del Iterable, Any, Type, Tuple, Iterator
del warnings
