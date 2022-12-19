from typing import Sequence
from core.typing.inputType import TYPE_Information
from core.mod.moduleTemplate import ModuleTemplate
from core.typing.moduleType import TYPE_Module, TYPE_Run_Env
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

    def run(self, env: TYPE_Run_Env):
        self.outMr.setTime(env["time"])
        self.outMr.clearCache()
        runFunc(self.outMr.putout, self.inMr.getInstances(),
                self.inMr.existOptionalInstancesName(), env)
        pass


if __name__ == "__main__":
    m = Module()
    #m.prepareData([])