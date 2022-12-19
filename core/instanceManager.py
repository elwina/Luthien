import commentjson as json
from typing import Any, MutableMapping, Sequence, TypedDict

from loguru import logger
from config.register import FIELD_LIST
from core.conf import getConfig
from core.typing.fieldType import Type_Instance_Declare

from core.typing.fieldType import  TYPE_Field
from core.typing.inputType import TYPE_Indata
from core.typing.linkType import TYPE_A_Link_Input, TYPE_Link_Declare


class _TYPE_A_Instance(TypedDict):
    instance: TYPE_Field
    declare: Type_Instance_Declare

TYPE_Instances = MutableMapping[str, _TYPE_A_Instance]


class InstanceManager():
    instances: TYPE_Instances={}

    def __init__(self):
        pass

    def createInstances(self):
        '''根据配置文件创建instances'''
        logger.info("Create instances according to config.")
        configInstances = getConfig()["instance"]
        for name in configInstances:
            inf = configInstances[name]
            Field = FIELD_LIST[inf["field"]]
            ins = Field()
            self.instances[name] = {"instance": ins, "declare": inf}

    def getInstance(self, name: str):
        '''获得instance'''
        return self.instances[name]["instance"]

    def defineInstance(self, name: str, methodName: str,
                       config: MutableMapping[str, Any], data: Any):
        '''使用define定义instance'''
        ins = self.getInstance(name)
        ins.define(methodName, config, data)

    def initDataIn(self):
        '''程序运行init阶段按init配置define instance'''
        logger.info("Init instances according to config")
        for name in self.instances:
            initInf=self.instances[name]["declare"]["init"]
            initWay=initInf["use"]
            match initWay:
                case "define":
                    defineData=initInf["define"]
                    self.defineInstance(name,defineData["method"],defineData["config"],defineData["data"])
                case "no":
                    pass

    def linkDataIn(self,linkInputList:Sequence[TYPE_A_Link_Input])->TYPE_Indata:
        '''根据link input配置indata'''
        indata:TYPE_Indata={}
        for linkInput in linkInputList:
            match linkInput["use"]:
                case "instance":
                    # 选择instance放入
                    if "instance" in linkInput:
                        insName=linkInput["instance"]
                        ins=self.getInstance(insName)
                        indata[linkInput["into"]]={
                            "method":"in",
                            "instance":ins
                            }
                    else:
                        logger.error("No instance said to use!")
                case "define":
                    pass
        return indata

    # def createAnoInstance(self,declare:Type_Instance_Declare)->TYPE_Field:
    #     Field = FIELD_LIST[declare["field"]]
    #     ins = Field()
    #     ins.define(declare["init"]["define"]["method"], config, data)
    #     pass
