from typing import TypedDict, Literal

from core.typing.fieldType import TYPE_FIRLD_LIST, TYPE_Field


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

    def __init__(self):
        pass

    # 第一步要创建field并且初始化
    def createField(self, fieldList: TYPE_FIRLD_LIST):
        re: TYPE_Fields = {}
        for fieldName in fieldList:
            fieldInstance = fieldList[fieldName]()
            re[fieldName] = {"instance": fieldInstance}

        self.fields = re

    def getFields(self, name):
        return self.fields[name]["instance"]