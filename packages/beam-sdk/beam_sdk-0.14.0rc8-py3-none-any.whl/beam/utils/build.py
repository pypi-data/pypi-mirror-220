import importlib
import json
import sys
import os
import inspect
import unittest.mock
import sys

from beam import App
from beam.utils.print import print_config
from typing import Optional
from types import ModuleType


class FallbackImport:
    def find_module(self, fullname, path=None):
        return self

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]

        # Use MagicMock for missing modules
        sys.modules[name] = unittest.mock.MagicMock(name=name)
        return sys.modules[name]


class AppBuilder:
    @staticmethod
    def _setup():
        if os.getenv("BEAM_IGNORE_IMPORTS_OFF", None) is None:
            sys.meta_path.insert(0, FallbackImport())

    @staticmethod
    def _find_app_in_module(app_module: ModuleType) -> None:
        app = None
        for member in inspect.getmembers(app_module):
            member_value = member[1]
            if isinstance(member_value, App):
                app = member_value
                break

        if app is not None:
            print_config(json.dumps(app()))
            return

        raise Exception("Beam app not found")

    @staticmethod
    def build(*, module_name: str, func_or_app_name: Optional[str]) -> None:
        AppBuilder._setup()

        if not os.path.exists(module_name):
            raise FileNotFoundError

        spec = importlib.util.spec_from_file_location(module_name, module_name)
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)

        sys.meta_path.pop(0)
        if func_or_app_name is None:
            AppBuilder._find_app_in_module(app_module)
            return

        try:
            _callable = getattr(app_module, func_or_app_name)
            print_config(json.dumps(_callable()))
        except AttributeError:
            raise


if __name__ == "__main__":
    """
    Usage:
        python3 -m beam.build <module_name.py>:<func_name>
            or
        python3 -m beam.build <module_name.py:<app_name>
    """

    app_handler = sys.argv[1]
    module_name = app_handler
    func_or_app_name = None
    try:
        module_name, func_or_app_name = app_handler.split(":")
    except ValueError:
        pass

    AppBuilder.build(module_name=module_name, func_or_app_name=func_or_app_name)
