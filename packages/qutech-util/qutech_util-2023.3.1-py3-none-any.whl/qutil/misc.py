import logging
import warnings
from contextlib import contextmanager


@contextmanager
def all_logging_disabled(highest_level=logging.CRITICAL):
    """
    A context manager that will prevent any logging messages
    triggered during the body from being processed.
    :param highest_level: the maximum logging level in use.
    This would only need to be changed if a custom level greater than CRITICAL
    is defined.

    https://gist.github.com/simon-weber/7853144
    """
    # two kind-of hacks here:
    #    * can't get the highest logging level in effect => delegate to the user
    #    * can't get the current module-level override => use an undocumented
    #       (but non-private!) interface

    previous_level = logging.root.manager.disable

    logging.disable(highest_level)

    try:
        yield
    finally:
        logging.disable(previous_level)


@contextmanager
def filter_warnings(action, category=Warning, lineno=0, append=False, *,
                    record=False, module=None):
    """A context manager that combines catching and filtering warnings."""
    with warnings.catch_warnings(record=record, module=module) as manager:
        warnings.simplefilter(action, category, lineno, append)
        try:
            yield manager
        finally:
            pass
