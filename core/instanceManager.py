from copy import deepcopy
from typing import Any, MutableMapping, Sequence, TypedDict
from core.typing.fieldType import Type_Instance_Declare
from core.typing.fieldType import TYPE_Field
from core.typing.inputType import TYPE_Indata
from core.typing.linkType import TYPE_Input_Declare
from core.typing.outputType import TYPE_Output_Action_Declare
from core.typing.recordType import TYPE_Record_Declare, TYPE_Recorder_TempEnv
from core.mod.outputManager import outputManager

from loguru import logger
from core.configGlobal import configGlobal
from core.envGlobal import envGlobal

logger = logger.bind(type="control.instance")


class _TYPE_A_Instance(TypedDict):
    """类中Instance类型定义"""

    instance: TYPE_Field
    declare: Type_Instance_Declare


_TYPE_Instances = MutableMapping[str, _TYPE_A_Instance]


class InstanceManager:
    instances: _TYPE_Instances = {}

    def __init__(self):
        pass

    def createInstances(self):
        """根据配置文件创建instances"""
        logger.info("Create instances according to config.")
        configInstances = configGlobal.getConfig()["instance"]
        from config.register import FIELD_LIST

        for item in configInstances:
            name = item["name"]
            inf = item
            Field = FIELD_LIST[inf["field"]]
            ins = Field()
            self.instances[name] = {"instance": ins, "declare": inf}

        logger.success("Successfully create instances.")

    def getInstance(self, name: str):
        """获得instance"""
        return self.instances[name]["instance"]

    def defineInstance(
        self, name: str, methodName: str, config: MutableMapping[str, Any], data: Any
    ):
        """使用define定义instance"""
        ins = self.getInstance(name)
        from config.register import IO_LIST

        ins.define(IO_LIST[methodName], config, data)

    def copyInstance(self, ins: TYPE_Field, src: str):
        """copy instance"""
        srcIns = self.getInstance(src)
        ins.data = deepcopy(srcIns.data)
        ins.iTM = deepcopy(srcIns.iTM)

    def initDataIn(self):
        """程序运行init阶段按init配置define instance"""
        logger.info("Init instances data according to config.")
        for name in self.instances:
            initInf = self.instances[name]["declare"]["init"]
            initWay = initInf["use"]
            match initWay:
                case "define":
                    defineData = initInf["define"]
                    self.defineInstance(
                        name,
                        defineData["method"],
                        defineData["config"],
                        defineData["data"],
                    )
                case "no":
                    pass
                case "copy":
                    src = initInf["copy"]
                    self.copyInstance(self.instances[name]["instance"], src)

        logger.success("Successfully init instances data")

    def linkDataIn(self, linkInputList: Sequence[TYPE_Input_Declare]) -> TYPE_Indata:
        """根据link input配置indata"""
        indata: TYPE_Indata = {}
        for linkInput in linkInputList:
            match linkInput["use"]:
                # 处理input declare
                case "instance":
                    # 选择instance放入
                    insName = linkInput["instance"]
                    ins = self.getInstance(insName)
                    indata[linkInput["into"]] = {"method": "in", "instance": ins}
                case "new":
                    # 匿名instance
                    insDeclare = linkInput["new"]
                    from config.register import FIELD_LIST

                    Field = FIELD_LIST[insDeclare["field"]]
                    ins = Field()
                    initInf = insDeclare["init"]
                    initWay = initInf["use"]
                    match initWay:
                        case "define":
                            from config.register import IO_LIST

                            defineData = initInf["define"]
                            ins.define(
                                IO_LIST[defineData["method"]],
                                defineData["config"],
                                defineData["data"],
                            )
                        case "no":
                            pass
                        case "copy":
                            src = initInf["copy"]
                            self.copyInstance(ins, src)

                    indata[linkInput["into"]] = {"method": "in", "instance": ins}
        return indata

    def updateFromOutput(
        self, actionList: Sequence[TYPE_Output_Action_Declare], outMr: outputManager
    ):
        """根据output action操作instance"""
        for action in actionList:
            catch = action["catch"]
            put = action["put"]
            time = envGlobal.epoch
            catchData = outMr.getOutputData(catch)
            if catchData is not None:
                self.instances[put]["instance"].iTM.store(catchData)
                logger.success(
                    "Output {out} is put out into instance {ins}.",
                    out=catch,
                    ins=action["put"],
                )
            else:
                logger.error("Catch instance not put out!")
            self.instances[put]["instance"].iTM.checkTime()

    def updateInsTime(self):
        """更新instance时间"""
        for name in self.instances:
            self.instances[name]["instance"].iTM.checkTime()

    def makeRecords(
        self, recordList: Sequence[TYPE_Record_Declare], ifStart=False, ifEnd=False
    ):
        """记录record"""
        linkDes = str(envGlobal.linkNowNum)
        if ifStart:
            linkDes = "start"
        if ifEnd:
            linkDes = "end"
        for record in recordList:
            self.makeARecord(
                record["catch"], record["method"], record["config"], linkDes
            )
        logger.success("Sucessfully make records in iMr.")

    def makeARecord(
        self, name: str, methodName: str, config: MutableMapping[str, Any], linkDes: str
    ):
        """使用record记录"""
        ins = self.getInstance(name)
        tempEnv: TYPE_Recorder_TempEnv = {
            "insName": name,
            "ifModule": False,
            "linkDes": linkDes,
        }
        from config.register import RECORDER_LIST

        ins.record(RECORDER_LIST[methodName], config, tempEnv)

    # 以下为待开发内容
    def _getIdCharRecord(self, idChar: str) -> Sequence[str]:
        """获得要在每个epoch前后记录的名单"""
        return list(
            filter(
                lambda x: self.instances[x]["declare"]["record"].__contains__(idChar),
                self.instances,
            )
        )

    def getStartRecord(self) -> Sequence[str]:
        return self._getIdCharRecord("s")

    def getEndRecord(self) -> Sequence[str]:
        return self._getIdCharRecord("e")
