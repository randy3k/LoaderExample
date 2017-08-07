import sys
import os
import importlib
from contextlib import contextmanager


loader_details = [
    (importlib.machinery.ExtensionFileLoader, importlib.machinery.EXTENSION_SUFFIXES),
    (importlib.machinery.SourceFileLoader, importlib.machinery.SOURCE_SUFFIXES),
    (importlib.machinery.SourcelessFileLoader, importlib.machinery.BYTECODE_SUFFIXES)
]


@contextmanager
def intercepting_imports(module_names):
    deps_path = os.path.join(os.path.dirname(__file__), "deps")
    finder = FilterFileFinder(module_names, deps_path, *loader_details)
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


class FilterFileFinder(importlib.machinery.FileFinder):
    def __init__(self, module_names, path, *loader_details):
        self._module_names = module_names
        super().__init__(path, *loader_details)

    def find_module(self, name, path=None):
        if name in self._module_names:
            return super().find_module(name)


module_names = ["foo"]
with intercepting_imports(module_names):
    from .src import *
