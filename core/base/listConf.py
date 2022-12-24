from typing import Any, Mapping, MutableMapping, Sequence
from config.register import IO_LIST
from core.base.listConfType import TYPE_LIST_CONF_DATA, TYPE_LIST_CONF_IN_DATA
from core.typing.ioType import TYPE_IO, TYPE_IO_DATA
from core.typing.recordType import TYPE_Recorder_Env
from core.utils.confType import TYPE_CONF_VALUE, generateInitDict

from typing_extensions import NotRequired, Required, TypedDict
'''
    [
        {
            "name": "string",
            "type": "string"|"int"|"float",
            "default": "x"
        }
    ]
'''


class ListConfBase:
    data: TYPE_LIST_CONF_DATA

    def __init__(self, typeName: str):
        self.typeName = typeName

    # 初始化并且附上默认值
    def init(self, list: TYPE_LIST_CONF_IN_DATA):
        self.key = [item["name"] for item in list]
        self.data: TYPE_LIST_CONF_DATA = generateInitDict(list)
        self.default(list)

    def default(self, list: TYPE_LIST_CONF_IN_DATA):
        for item in list:
            if "default" in item:
                self.data[item["name"]] = item["default"]

    def setOne(self, key: str, value: str):
        self.data[key] = value

    def getOne(self, key: str):
        return self.data[key]

    def setter(self, indata: dict):
        for item in indata:
            if item in self.key:
                self.data[item] = indata[item]

    # define是重要函数
    def define(self, method: TYPE_IO, config: MutableMapping[str, Any],
               data: Any):
        config["outListConf"] = True
        re = method({"config": config, "oldData": self.data, "newData": data})
        self.data = re["newData"]

    def record(self, methodName: str, config: MutableMapping[str, Any],
               env: TYPE_Recorder_Env):
        pass
