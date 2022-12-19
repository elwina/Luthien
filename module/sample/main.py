from typing import Sequence
from core.typing.inputType import TYPE_Information
from core.mod.moduleTemplate import ModuleTemplate
from core.typing.moduleType import TYPE_Module
from core.typing.fieldType import TYPE_Field
from module.sample.run import sampleRun as runFunc

MODULE_INSTANCE_INF: TYPE_Information = {
    "dem": {
        "required": True
    },
    "sampleUni": {
        "required": True
    },
    "water": {
        "required": False
    }
}


class Module(ModuleTemplate, TYPE_Module):

    def __init__(self):
        super().__init__("sample", MODULE_INSTANCE_INF)

    def run(self):
        runFunc(self.inMr.getInstances(),
                self.inMr.existOptionalInstancesName())
        pass


if __name__ == "__main__":
    m = Module()
    #m.prepareData([])