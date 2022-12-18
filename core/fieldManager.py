import commentjson as json
from typing import Any, MutableMapping, TypedDict, Literal

from loguru import logger
from config.path import DATA_JSON_PATH
from core.typing.dataType import TYPE_DATA_JSON

from core.typing.fieldType import TYPE_FIELD_LIST, TYPE_Field


class _TYPE_A_Field(TypedDict):
    instance: TYPE_Field


TYPE_Fields = dict[str, _TYPE_A_Field]


class FieldManager():
    '''
        fields
        {
            name: {
                instance: fieldObject
            },
        }
    '''

    field: TYPE_Fields

    def __init__(self):
        pass

    # 第一步要创建field并且初始化
    def createField(self, fieldList: TYPE_FIELD_LIST):
        re: TYPE_Fields = {}
        for fieldName in fieldList:
            fieldInstance = fieldList[fieldName]()
            re[fieldName] = {"instance": fieldInstance}

        self.fields = re

    def getFields(self, name):
        return self.fields[name]["instance"]

    def defineField(self, name, methodName: str,
                    config: MutableMapping[str, Any], data: Any):
        ins = self.getFields(name)
        ins.define(methodName, config, data)

    # Define阶段数据
    def initDataIn(self):
        logger.info("Read Data Json {path}", path=DATA_JSON_PATH)
        with open(DATA_JSON_PATH) as fp:
            initData: TYPE_DATA_JSON = json.load(fp)
            for name in initData:
                self.defineField(name, initData[name]["method"],
                                 initData[name]["config"],
                                 initData[name]["data"])
