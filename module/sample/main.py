from typing import Sequence
from core.typing.inputType import TYPE_Information
from core.mod.moduleTemplate import ModuleTemplate
from core.typing.moduleType import TYPE_Module
from core.typing.fieldType import TYPE_Field
from core.typing.outputType import TYPE_Output_Information
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

MODULE_OUTPUT_INSTANCE_INF: TYPE_Output_Information = {"water": {}}


class Module(ModuleTemplate, TYPE_Module):

    def __init__(self):
        super().__init__("sample", MODULE_INSTANCE_INF,
                         MODULE_OUTPUT_INSTANCE_INF)

    def run(self):
        self.outMr.clearCache()
        runFunc(self.outMr.putout, self.inMr.getInstances(),
                self.inMr.existOptionalInstancesName())
        pass


if __name__ == "__main__":
    m = Module()
    #m.prepareData([])