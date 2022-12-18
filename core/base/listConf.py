from typing import Any, Mapping, MutableMapping, Sequence, TypedDict
from config.register import IO_LIST
from core.typing.ioType import TYPE_IO, TYPE_IO_DATA
from core.utils.confType import TYPE_CONF_VALUE, generateInitDict

from typing_extensions import NotRequired, Required
'''
    [
        {
            "name": "string",
            "type": "string"|"int"|"float",
            "default": "x"
        }
    ]
'''


class TYPE_LIST_CONF_IN_A_DATA(TypedDict, total=False):
    name: Required[str]
    type: Required[str]
    default: TYPE_CONF_VALUE


TYPE_LIST_CONF_IN_DATA = Sequence[TYPE_LIST_CONF_IN_A_DATA]

TYPE_LIST_CONF_DATA = MutableMapping[str, TYPE_CONF_VALUE]


class ListConfBase:

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

    def setterOne(self, key: str, value: str):
        self.data[key] = value

    def getterOne(self, key: str):
        return self.data[key]

    def setter(self, indata: dict):
        for item in indata:
            if item in self.key:
                self.data[item] = indata[item]

    # define是重要函数
    def define(self, methodName: str, config: MutableMapping[str, Any],
               data: Any):
        method = IO_LIST[methodName]
        config["outListConf"] = True
        re = method({"config": config, "oldData": self.data, "newData": data})
        self.data = re["newData"]


if __name__ == "__main__":
    test = [{
        "name": "teststring",
        "type": "string"
    }, {
        "name": "tesint",
        "type": "int"
    }, {
        "name": "testfloat",
        "type": "float",
        "default": 0.25
    }]
    lc = ListConfBase("test")
    lc.init(test)
    lc.default(test)

    lc.define("json", {
        "outListConf": True,
        "inFile": True,
        "inFilePath": "data/test.json"
    }, None)
    pass
