import sys
import os
from contextlib import contextmanager


@contextmanager
def intercepting_imports(module_names):
    deps_path = os.path.join(os.path.dirname(__file__), "deps")
    sys.path.insert(0, deps_path)

    # save the original modules to prevent overwritte modules of the same name
    original_modules = {}
    for m in module_names:
        if m in sys.modules:
            original_modules[m] = sys.modules[m]
        else:
            original_modules[m] = None
    try:
        yield
    finally:
        if deps_path in sys.path:
            sys.path.remove(deps_path)

        # restore the original modules
        for m in module_names:
            if original_modules[m]:
                sys.modules[m] = original_modules[m]
            else:
                if m in sys.modules:
                    del sys.modules[m]


module_names = ["foo"]
with intercepting_imports(module_names):
    from .src import *
