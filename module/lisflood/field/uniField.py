from core.base.listConfType import TYPE_LIST_CONF_IN_DATA
from core.typing.fieldType import TYPE_Field
from core.base.listConf import ListConfBase

UNI_INPUT_DICT_DEFAULT: TYPE_LIST_CONF_IN_DATA = [{
    "name": "version",
    "type": "int",
    "default": 1
}, {
    "name": "rainFromConf",
    "type": "int",
    "default": 0
}, {
    "name": "rainBase",
    "type": "int",
    "default": 0
}, {
    "name": "rainAddPerhour",
    "type": "int",
    "default": 0
}, {
    "name": "simTime",
    "type": "int",
    "default": 60 * 60 * 3
}, {
    "name": "saveInt",
    "type": "int",
    "default": 60 * 60
}, {
    "name": "fpfric",
    "type": "float",
    "default": 0.06
}, {
    "name": "recordNum",
    "type": "int",
    "default": 3
}]


class UniField(ListConfBase, TYPE_Field):

    def __init__(self):
        super(UniField, self).__init__("uniInputField")
        self.init(UNI_INPUT_DICT_DEFAULT)
