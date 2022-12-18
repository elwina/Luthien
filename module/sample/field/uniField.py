from core.base.listConf import ListConfBase
from core.typing.fieldType import TYPE_Field

UNI_INPUT_DICT_DEFAULT = [{
    "name": "version",
    "type": "int",
    "default": 1
}, {
    "name": "authCode",
    "type": "string",
    "default": "aaas1"
}]


class UniField(ListConfBase, TYPE_Field):

    def __init__(self):
        super(UniField, self).__init__("uniInputField")
        self.init(UNI_INPUT_DICT_DEFAULT)

    def test(self):
        print(self.getterOne("version"))


if __name__ == "__main__":
    pass
