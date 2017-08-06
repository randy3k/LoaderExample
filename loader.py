import sys
import os
import importlib
from contextlib import contextmanager


@contextmanager
def intercepting_imports(modules):
    finder = FilterFinder(modules)
    sys.meta_path.insert(0, finder)
    try:
        yield
    finally:
        if finder in sys.meta_path:
            sys.meta_path.remove(finder)


class FilterFinder:
    def __init__(self, modules):
        self._modules = modules
        self.deps_path = os.path.join(os.path.dirname(__file__), "deps")

    def find_module(self, name, path=None):
        if name in self._modules:
            path = os.path.join(self.deps_path, name)
            if os.path.isdir(path):
                return importlib.machinery.SourceFileLoader(name, os.path.join(path, "__init__.py"))
            else:
                return importlib.machinery.SourceFileLoader(name, path + ".py")

modules = ["foo"]
with intercepting_imports(modules):
    from .src import *
