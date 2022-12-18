import commentjson as json
from typing import Any, MutableMapping, TypedDict

from loguru import logger
from config.register import FIELD_LIST
from core.conf import getConfig
from core.typing.configType import Type_Instance_Declare

from core.typing.fieldType import  TYPE_Field


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
