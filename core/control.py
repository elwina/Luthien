from core.link.linkGenerator import LinkGenerator
from importlib import import_module

from core.link.moduleInf import ModuleInf
from core.coupler import Coupler


class Control():

    def __init__(self, Global):
        self.timestep = 0
        self.linkSheet = self.getLink()["link"]
        self.Global = Global

    def getLink(self):
        lg = LinkGenerator()
        return lg.getLink()

    def run(self):
        for action in self.linkSheet:
            moduleInf: ModuleInf = self.Global["moduleInformation"]
            mo = moduleInf.getModule(action["module"])
            print(mo.name)

            cp = Coupler(action)
