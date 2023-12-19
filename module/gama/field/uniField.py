from core.base.listConfType import TYPE_LIST_CONF_IN_DATA
from core.typing.fieldType import TYPE_Field
from core.base.listConf import ListConfBase

UNI_INPUT_DICT_DEFAULT: TYPE_LIST_CONF_IN_DATA = [
    {"name": "version", "type": "int", "default": 1},
    {"name": "total_people", "type": "int", "default": 1000},
]


class UniField(ListConfBase, TYPE_Field):
    def __init__(self):
        super(UniField, self).__init__("uniInputField")
        self.init(UNI_INPUT_DICT_DEFAULT)
