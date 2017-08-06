import sys
import os
import importlib
from contextlib import contextmanager


@contextmanager
def intercepting_imports(module_names):
    finder = FilterFinder(module_names)
    sys.meta_path.insert(0, finder)

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
        if finder in sys.meta_path:
            sys.meta_path.remove(finder)

        # restore the original modules
        for m in module_names:
            if original_modules[m]:
                sys.modules[m] = original_modules[m]
            else:
                if m in sys.modules:
                    del sys.modules[m]


class FilterFinder:
    def __init__(self, module_names):
        self._modules = module_names
        self.deps_path = os.path.join(os.path.dirname(__file__), "deps")

    def find_module(self, name, path=None):
        if name in self._modules:
            path = os.path.join(self.deps_path, name)
            if os.path.isdir(path):
                return importlib.machinery.SourceFileLoader(name, os.path.join(path, "__init__.py"))
            else:
                return importlib.machinery.SourceFileLoader(name, path + ".py")


module_names = ["foo"]
with intercepting_imports(module_names):
    from .src import *
