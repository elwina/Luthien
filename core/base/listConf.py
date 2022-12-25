from typing import Any, MutableMapping
from core.base.listConfType import TYPE_LIST_CONF_DATA, TYPE_LIST_CONF_IN_DATA
from core.typing.ioType import TYPE_IO, TYPE_IO_DATA
from core.typing.recordType import TYPE_Recorder, TYPE_Recorder_Env, TYPE_Recorder_TempEnv
from core.utils.confType import generateInitDict


class ListConfBase:
    '''基础类型:ListConf,处理一一对应的配置关系'''
    '''
    TYPE_LIST_CONF_IN_DATA形如
    [
        {
            "name": "string",
            "type": "string"|"int"|"float",
            "default": "x"
        }
    ]
    '''
    '''
    data:TYPE_LIST_CONF_DATA形如
    {"conf1":"somevalue"}
    '''

    data: TYPE_LIST_CONF_DATA

    # 初始化函数
    def __init__(self, typeName: str):
        self.typeName = typeName

    def init(self, list: TYPE_LIST_CONF_IN_DATA):
        '''每个子类必须在__init__中调用此函数'''
        self.key = [item["name"] for item in list]
        self.data: TYPE_LIST_CONF_DATA = generateInitDict(list)
        self.default(list)

    def default(self, list: TYPE_LIST_CONF_IN_DATA):
        '''根据list设置默认值'''
        for item in list:
            if "default" in item:
                self.data[item["name"]] = item["default"]

    # 接口函数
    def define(self, method: TYPE_IO, config: MutableMapping[str, Any],
               data: Any):
        config["outListConf"] = True
        re = method({"config": config, "oldData": self.data, "newData": data})
        self.data = re["newData"]

    def record(self, method: TYPE_Recorder, config: MutableMapping[str, Any],
               tempEnv: TYPE_Recorder_TempEnv):
        method({"config": config, "data": self.data, "tempEnv": tempEnv})

    # 辅助函数
    def setOne(self, key: str, value: str):
        '''设置值'''
        self.data[key] = value

    def getOne(self, key: str):
        '''获取值'''
        return self.data[key]

    def setter(self, indata: dict):
        '''批量设置值'''
        for item in indata:
            if item in self.key:
                self.data[item] = indata[item]
