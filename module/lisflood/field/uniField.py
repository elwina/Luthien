from core.base.listConfType import TYPE_LIST_CONF_IN_DATA
from core.typing.fieldType import TYPE_Field
from core.base.listConf import ListConfBase

UNI_INPUT_DICT_DEFAULT: TYPE_LIST_CONF_IN_DATA = [
    {
        "name": "version",
        "type": "int",
        "default": 1
    },
    {
        "name": "simTime",
        "type": "int",
        "default": 60 * 60 * 3
    },
    {
        "name": "saveInt",  # par中参数
        "type": "int",
        "default": 60 * 60
    },
    {
        "name": "fpfric",  # par中参数
        "type": "float",
        "default": 0.06
    },
    {
        "name": "recordNum",  # 记录下的文件总数
        "type": "int",
        "default": 3
    },
    # 雨水相关参数
    {
        "name": "rainFromFile",  # 从file中得到雨水文件 # 优先级高
        "type": "string",
        "default": ""
    },
    {
        "name": "rainFromConf",  # 用下面的参数模拟雨水文件
        "type": "int",
        "default": 0
    },
    {
        "name": "rainBase",
        "type": "int",
        "default": 0
    },
    {
        "name": "rainAddPerhour",
        "type": "int",
        "default": 0
    },
    # 边界条件
    {
        "name": "bciFromFile",
        "type": "string",
        "default": ""
    },
    {
        "name": "bdyFromFile",
        "type": "string",
        "default": ""
    },
    # 来自swmm的点溢流
    {
        "name": "bciFromPoint",
        "type": "int",
        "default": 0
    }
]


class UniField(ListConfBase, TYPE_Field):

    def __init__(self):
        super(UniField, self).__init__("uniInputField")
        self.init(UNI_INPUT_DICT_DEFAULT)
