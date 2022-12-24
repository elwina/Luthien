from typing import MutableMapping
from core.typing.linkType import TYPE_Link_Declare
from core.typing.moduleType import TYPE_Module

from core.instanceManager import InstanceManager
from core.linkManager import LinkManager

from loguru import logger
from core.envGlobal import envGlobal


class Controller():
    lMr: LinkManager
    iMr: InstanceManager

    modules: MutableMapping[str, TYPE_Module] = {}
    nowLinkNum: int
    mo: TYPE_Module

    def __init__(self):
        self.initialize()

    def initialize(self):
        '''Controller初始化'''
        logger.info("Controller starts initializing.")

        # iMr初始化
        self.iMr = InstanceManager()
        self.iMr.createInstances()
        self.iMr.initDataIn()

        # lMr初始化
        self.lMr = LinkManager()

        # 模块初始化
        from config.register import MODULE_LIST
        for moName in MODULE_LIST:
            logger.info("Create Module {module_name}.", module_name=moName)
            self.modules[moName] = MODULE_LIST[moName]()
        logger.success("All modules created.")

    def run(self):
        '''启动函数'''
        for epoch, links in self.lMr.geneEpochs():
            logger.info("Epoch {num} start.", num=epoch)

            for link in links:
                logger.info("Now process module {module_name}",
                            module_name=link["module"])
                self.mo = self.modules[link["module"]]

                # 检查是否需要跑
                if self.lMr.ifLinkRun():
                    # 需要跑
                    logger.info("Put data in and run module {module_name}",
                                module_name=link["module"])
                    self.dataIn()
                    self.runOne()
                else:
                    # 不需要跑,直接处理数据
                    logger.info("No Run it")

                self.dealOut()
                self.recordData()

            logger.success("Epoch {num} end.", num=epoch)
        logger.success("Run done.")

    def dataIn(self):
        logger.debug("Put instances into module.")
        self.mo.prepareData(self.iMr.linkDataIn(self.lMr.getInputDeclare()))

    def runOne(self):
        logger.debug("Run the module.")
        self.mo.run()

    def dealOut(self):
        logger.debug("Deal with the module output.")
        self.iMr.updateFromOutput(self.lMr.getOutputAction(), self.mo.outMr)

    def recordData(self):
        logger.debug("Record inside instances.")
        self.mo.outMr.makeRecords(self.lMr.getRecordInside())
        logger.debug("Record instances.")
        self.iMr.makeRecords(self.lMr.getRecordDeclare())

    def updateEnv(self):
        logger.debug("update env from Controller.")
