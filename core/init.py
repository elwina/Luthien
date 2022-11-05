import json
from core.link.moduleInf import ModuleInf


def getConfig():
    with open("config/basic.json") as fp:
        return json.load(fp)


def init(Global):
    Global["BasicConfig"] = getConfig()
    moduleList = Global["BasicConfig"]["moduleList"]
    Global["moduleInformation"] = ModuleInf(moduleList)