from typing import MutableMapping
from core.instanceManager import InstanceManager
from core.linkManager import LinkManager
from config.register import MODULE_LIST, FIELD_LIST
from loguru import logger
from core.typing.linkType import TYPE_Link_Declare

from core.typing.moduleType import TYPE_Module, TYPE_Run_Env
from core.typing.recordType import TYPE_Recorder_Env


class Control():
    lMr: LinkManager
    iMr: InstanceManager

    modules: MutableMapping[str, TYPE_Module] = {}
    nowModule: str
    nowLink: TYPE_Link_Declare
    nowLinkNum: int

    def __init__(self, Global):
        self.initialize()

    def initialize(self):
        self.iMr = InstanceManager()
        self.iMr.createInstances()
        self.iMr.initDataIn()

        self.lMr = LinkManager()

        for moName in MODULE_LIST:
            logger.info("Create Module {module_name}", module_name=moName)
            self.modules[moName] = MODULE_LIST[moName]()

    def run(self):
        for epoch in range(self.lMr.getTotalEpochs()):
            logger.info("Epoch {num} start.", num=epoch)

            for (i, link) in enumerate(self.lMr.getLinkDeclare()):
                logger.info("Start Run Module {module_name}",
                            module_name=link["module"])
                self.nowModule = link["module"]
                self.nowLink = link
                self.nowLinkNum = i

                self.dataIn()
                self.runOne()
                self.dealOut()
                self.recordData()

            self.lMr.timeAdd()
            logger.info("Epoch {num} end.", num=epoch)

    def dataIn(self):
        mo = self.modules[self.nowModule]
        mo.prepareData(self.iMr.linkDataIn(self.nowLink["input"]))

    def runOne(self):
        mo = self.modules[self.nowModule]
        mo.run(self.generateEnv())

    def dealOut(self):
        mo = self.modules[self.nowModule]
        self.iMr.updateFromOutput(
            self.lMr.getOutputAction(self.nowLink["output"]), mo.outMr,
            self.lMr.getTime())

    def recordData(self):
        mo = self.modules[self.nowModule]
        #mo.outMr.makeRecords(self.nowLink["recordInside"],self.generateRecorderEnv())
        self.iMr.makeRecords(self.nowLink["record"],
                             self.generateRecorderEnv())

    def generateEnv(self) -> TYPE_Run_Env:
        return {
            "timestep": self.lMr.timestep,
            "timeUnit": self.lMr.timeUnit,
            "time": self.lMr.getTime()
        }

    def generateRecorderEnv(self) -> TYPE_Recorder_Env:
        filename = "output/" + self.nowModule + '-' + str(
            self.nowLinkNum) + '-' + str(self.lMr.getTime())

        return {"time": self.lMr.getTime(), "pre": filename}
