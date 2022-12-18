from typing import Sequence
from core.field.demField import DemField
from core.template.moduleTemplate import ModuleTemplate
from core.typing.moduleType import TYPE_Module
from core.typing.fieldType import TYPE_Field
from module.lisflood.run import sampleRun as runFunc


class Module(ModuleTemplate, TYPE_Module):
    inputFieldsNames: list[str] = ["dem", "sampleUni"]
    inputFields: list[TYPE_Field]

    inputFieldsRequired: Sequence[str] = ["dem", "sampleUni"]
    inputFieldsOptional: Sequence[str] = []
    internalOutput: Sequence[str] = []

    def __init__(self):
        super(Module, self).__init__("sample")

    def prepareData(self, list: list[TYPE_Field]):
        self.inputFields = list
        pass

    def run(self):
        runFunc(self.inputFields[0])
        pass
