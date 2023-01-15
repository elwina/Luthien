from typing import  Mapping, MutableMapping, Sequence
from typing_extensions import Required, TypedDict

'''
    配置项的类型,支持string,float,int
'''

TYPE_CONF_VALUE=str|int|float

def generateInitValue(type:str):
    match type:
        case "int":
            return 0
        case "float":
            return 0.0
        case "string":
            return ""
        case default:
            return ""




class _TYPE_A_INIT_DICT(TypedDict,total=False):
    name:Required[str]
    type:Required[str]

_TYPE_INIT_DICT=Sequence[_TYPE_A_INIT_DICT]
'''
_TYPE_A_INIT_DICT形如
    [
        {
            "name": "string",
            "type": "string"|"int"|"float"
        }
    ]
'''


def generateInitDict(list:_TYPE_INIT_DICT)->dict[str, TYPE_CONF_VALUE]:
    '''根据init dict生成dict'''
    return dict(zip([item["name"] for item in list],[generateInitValue(item["type"]) for item in list]))