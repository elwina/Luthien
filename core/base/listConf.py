from typing import Any
from core.utils.confType import generateInitDict
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

    def __init__(self, typeName: str):
        self.typeName = typeName

    # 初始化并且附上默认值
    def init(self, list: list[dict]):
        self.key = [item["name"] for item in list]
        self.data: dict[str, Any] = generateInitDict(list)
        self.default(list)

    def default(self, list: list[dict]):
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
