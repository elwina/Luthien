from importlib import import_module
from types import ModuleType

from core.template.moduleTemplate import ModuleTemplate


class ModuleInf():

    def __init__(self, list):
        inf = {}
        for module_name in list:
            mo = import_module("module." + str(module_name) + ".main")
            inf[module_name] = mo.Module()
        self.inf = inf

    def getModule(self, name) -> ModuleTemplate:
        return self.inf[name]
