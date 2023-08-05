"""This is an interface definition which is used by typechecking because lazy importing currently does no allow that as
described in https://scientific-python.org/specs/spec-0001."""

__version__ = "typing_interface_version_dummy"

# necessary due to https://peps.python.org/pep-0484/#stub-files
from . import caching as caching
from . import const as const
from . import functools as functools
from . import io as io
from . import itertools as itertools
from . import linalg as linalg
from . import matlab as matlab
from . import misc as misc
from . import pandas_tools as pandas_tools
from . import parallel as parallel
from . import plotting as plotting
from . import qcodes as qcodes
from . import qi as qi
from . import random as random
from . import typecheck as typecheck

# use this code to update the stub
def _gen_stub(root=None):
    import pathlib
    if root is None:
        root = pathlib.Path(__file__).parent
    sub_modules = []
    for module in root.glob('*.py'):
        module_name = module.stem
        if module_name.startswith('_'):
            continue
        sub_modules.append(module_name)

    imports = '\n'.join(f'from . import {module_name} as {module_name}' for module_name in sub_modules)
    return imports
