from __future__ import annotations
import pkgutil
import inspect
import importlib
import traceback

from ml4proflow import modules
from ml4proflow.exceptions import NoSuchModule


def find_and_import_framework_modules() -> dict[str, set[str]]:
    found_basicmodules = []
    found_sinks = []
    found_sources = []
    found_modules = []
    search_modules = ['ml4proflow.modules', 'ml4proflow.modules_extra']
    try:
        mod_top_module = importlib.import_module('ml4proflow_mods')
        mods = pkgutil.iter_modules(mod_top_module.__path__)
        for mod in mods:
            search_modules.append("ml4proflow_mods.%s.modules" % mod.name)
    except ModuleNotFoundError:
        print("No Mods installed")
    for module in search_modules:
        # just ignore modules that generate an exception
        try:
            m = importlib.import_module(module)
            classes = inspect.getmembers(m, inspect.isclass)
            for name, c in classes:
                if issubclass(c, modules.BasicModule):
                    found_basicmodules.append(c)
                if issubclass(c, modules.Module):
                    found_modules.append(c)
                if issubclass(c, modules.SinkModule):
                    found_sinks.append(c)
                if issubclass(c, modules.SourceModule):
                    found_sources.append(c)
        except Exception:
            print("Exception while loading %s" % module)
            print(traceback.format_exc())
    return {"basicmodules": set(found_basicmodules),
            "sinks": set(found_sinks),
            "sources": set(found_sources),
            "modules": set(found_modules)}


def find_by_name(module_ident: str) -> type[modules.BasicModule]:
    module_name, class_name = module_ident.rsplit('.', 1)
    module_module = importlib.import_module(module_name)
    try:
        module_class = getattr(module_module, class_name)
    except AttributeError:
        err_msg = ("There is no Module ('%s') available, you may need" +
                   " to install an additional package") % module_ident
        raise NoSuchModule(err_msg) from None
    if not issubclass(module_class, modules.BasicModule):
        raise NoSuchModule("Error: %s" % module_ident)
    return module_class
