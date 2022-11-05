from importlib import import_module


class ModuleInf():

    def __init__(self, list):
        inf = {}
        for module_name in list:
            mo = import_module("module." + str(module_name) + ".main")
            inf[module_name] = mo
        self.inf = inf

    def getModule(self, name):
        return self.inf[name]
