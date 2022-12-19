from typing import Sequence
import commentjson as json
from loguru import logger
from core.conf import getConfig
from core.typing.linkType import TYPE_Link_Declare
from core.typing.outputType import TYPE_A_Output_Action


class LinkManager:
    linkDeclare: Sequence[TYPE_Link_Declare]

    timestep: int
    timeUnit: str
    timeEpoch: int

    timenow: int

    def __init__(self):
        self.init()

    def init(self):
        logger.info("Load linkDeclare from config.")
        self.linkDeclare = getConfig()["link"]

        logger.info("Load timeConfig from config.")
        basicConfig = getConfig()["basic"]
        self.timestep = basicConfig["timestep"]
        self.timeUnit = basicConfig["timeUnit"]
        self.timeEpoch = basicConfig["timeEpoch"]

        self.timenow = 0
        logger.info("Set time to 0.")

    def getTime(self):
        return self.timenow

    def getTotalEpochs(self):
        return self.timeEpoch

    def getLinkDeclare(self) -> Sequence[TYPE_Link_Declare]:
        time = self.timenow
        return list(
            filter(lambda x: time % x["timeInter"] == 0, self.linkDeclare))

    def timeAdd(self):
        self.timenow = self.timenow + 1

    def getOutputAction(
        self, actionList: Sequence[TYPE_A_Output_Action]
    ) -> Sequence[TYPE_A_Output_Action]:
        time = self.timenow
        return list(filter(lambda x: time % x["timeInter"] == 0, actionList))
