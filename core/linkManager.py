from tqdm import tqdm

from typing import Optional, Sequence
from core.typing.linkType import TYPE_Link_Declare
from core.typing.outputType import TYPE_Output_Action_Declare

from loguru import logger
from core.configGlobal import configGlobal
from core.envGlobal import envGlobal


class LinkManager:
    linkDeclare: Sequence[TYPE_Link_Declare]

    timestep: int
    timeUnit: str
    allEpochs: int

    timenow: int
    nowLinkNum: int

    pbar: tqdm

    def __init__(self):
        self.init()

    def init(self):
        logger.info("Load link declare from config.")
        self.linkDeclare = configGlobal.getConfig()["link"]

        logger.info("Load time config from config.")
        basicConfig = configGlobal.getConfig()["basic"]
        self.timestep = basicConfig["timestep"]
        self.timeUnit = basicConfig["timeUnit"]
        self.allEpochs = basicConfig["timeEpoch"]
        # 定义env config
        envGlobal.timestep = self.timestep
        envGlobal.timeUnit = self.timeUnit

        logger.info("Set time to 0.")
        self.timenow = 0
        self.nowLinkNum = 0
        self.updateEnv()

        self.pbar = tqdm(total=self.allEpochs * self.linkDeclare.__len__(),
                         disable=True)

    def geneEpochs(self):
        '''总轮数生成器'''
        for i in range(self.allEpochs):
            self.timenow = i
            self.updateEnv()

            def geneLink():
                for num, link in enumerate(self.linkDeclare):
                    self.nowLinkNum = num
                    self.updateEnv()
                    yield link
                    self.pbar.update(1)

            yield i, geneLink()

    def ifLinkRun(self, num: Optional[int] = None) -> bool:
        '''返回第num个link是否需要跑'''
        if num is None: num = self.nowLinkNum
        time = self.timenow
        if time % self.linkDeclare[num]["timeInter"] == 0:
            return True
        else:
            return False

    def getInputDeclare(self, num: Optional[int] = None):
        time = self.timenow
        if num is None: num = self.nowLinkNum
        inputList = self.linkDeclare[num]["input"]
        return inputList

    def getOutputAction(
            self,
            num: Optional[int] = None) -> Sequence[TYPE_Output_Action_Declare]:
        time = self.timenow
        if num is None: num = self.nowLinkNum
        actionList = self.linkDeclare[num]["output"]
        return list(filter(lambda x: time % x["timeInter"] == 0, actionList))

    def getRecordInside(self, num: Optional[int] = None):
        time = self.timenow
        if num is None: num = self.nowLinkNum
        recordInsideList = self.linkDeclare[num]["recordInside"]
        recordInsideList = list(
            filter(
                lambda x: not (x["onlyrun"] == True and self.ifLinkRun() ==
                               False), recordInsideList))
        return recordInsideList

    def getRecordDeclare(self, num: Optional[int] = None):
        time = self.timenow
        if num is None: num = self.nowLinkNum
        recordList = self.linkDeclare[num]["record"]
        return recordList

    def updateEnv(self):
        logger.debug("Update env from lMr.")
        envGlobal.epoch = self.timenow
        envGlobal.linkNowNum = self.nowLinkNum
        envGlobal.moduleNow = self.linkDeclare[self.nowLinkNum]["module"]

    def timeParser(self):
        '''[待开发]解析时间何时运行'''
        pass
