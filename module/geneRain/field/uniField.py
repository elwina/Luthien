from core.base.listConfType import TYPE_LIST_CONF_IN_DATA
from core.typing.fieldType import TYPE_Field
from core.base.listConf import ListConfBase

UNI_INPUT_DICT_DEFAULT: TYPE_LIST_CONF_IN_DATA = [{
    "name": "version",
    "type": "int",
    "default": 1
}, {
    "name": "A1",
    "type": "float",
    "default": 134.5106
}, {
    "name": "A2",
    "type": "float",
    "default": 0.4784
}, {
    "name": "P",
    "type": "float",
    "default": 20
}, {
    "name": "B",
    "type": "float",
    "default": 32.0692
}, {
    "name": "C",
    "type": "float",
    "default": 1.1947
}, {
    "name": "r",
    "type": "float",
    "default": 0.4
}, {
    "name": "totalMinutes",
    "type": "int",
    "default": 150
}, {
    "name": "rainGage",
    "type": "string",
    "default": "STA1"
}, {
    "name": "date",
    "type": "string",
    "default": "2022 06 01"
}]


class UniField(ListConfBase, TYPE_Field):

    def __init__(self):
        super(UniField, self).__init__("uniInputField")
        self.init(UNI_INPUT_DICT_DEFAULT)
