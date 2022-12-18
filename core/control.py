from core.instanceManager import InstanceManager
from core.linkGenerator import LinkGenerator
from config.register import MODULE_LIST, FIELD_LIST
from loguru import logger

from core.typing.linkType import TYPE_A_Link
from core.typing.moduleType import TYPE_Module


class Control():
    lGr: LinkGenerator
    iMr: InstanceManager

    modules: dict[str, TYPE_Module] = {}
    nowModule: str
    nowAction: TYPE_A_Link

    def __init__(self, Global):
        self.timestep = 0
        self.getLink()
        self.Global = Global

        self.initialize()

    def getLink(self):
        lGr = LinkGenerator()
        self.linkSheet = lGr.getLink()

    def initialize(self):
        self.iMr = InstanceManager()
        self.iMr.createInstances()
        self.iMr.initDataIn()

        for moName in MODULE_LIST:
            logger.info("Create Module {module_name}", module_name=moName)
            self.modules[moName] = MODULE_LIST[moName]()

    def run(self):
        for action in self.linkSheet:
            logger.info("Start Run Module {module_name}",
                        module_name=action["module"])
            self.nowModule = action["module"]
            self.nowAction = action
            self.dataIn()
            self.runOne()

    def runOne(self):
        mo = self.modules[self.nowModule]
        mo.run()

    def dataIn(self):
        mo = self.modules[self.nowModule]
        requireFields = list(
            map(lambda fieldName: self.iMr.getInstance(fieldName),
                mo.inputFieldsNames))
        mo.prepareData(requireFields)
