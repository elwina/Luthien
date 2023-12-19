from core.typing.moduleType import TYPE_Module
from core.mod.moduleTemplate import ModuleTemplate

from module.euluc.information import MODULE_INSTANCE_INF, MODULE_NAME, MODULE_OUTPUT_INSTANCE_INF
from module.euluc.run import eulucRun as runFunc


class Module(ModuleTemplate, TYPE_Module):

    def __init__(self):
        super().__init__(MODULE_NAME, MODULE_INSTANCE_INF,
                         MODULE_OUTPUT_INSTANCE_INF)

    def run(self):
        self.outMr.clearCache()
        runFunc(self.outMr.putout, self.inMr.getInstances(),
                self.inMr.existOptionalInstancesName())
