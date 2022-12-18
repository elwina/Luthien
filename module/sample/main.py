from typing import Sequence
from core.mod.moduleTemplate import ModuleTemplate
from core.typing.moduleType import TYPE_Module
from core.typing.fieldType import TYPE_Field
from module.sample.run import sampleRun as runFunc


class Module(ModuleTemplate, TYPE_Module):
    inputFieldsNames: list[str] = ["dem", "sampleUni"]
    inputFields: list[TYPE_Field]

    inputFieldsRequired: Sequence[str] = ["dem", "sampleUni"]
    inputFieldsOptional: Sequence[str] = []
    internalOutput: Sequence[str] = []

    def __init__(self):
        super(Module, self).__init__("sample")

    def prepareData(self, list: list[TYPE_Field]):
        '''传入数据'''
        self.inputFields = list
        pass

    def run(self):
        runFunc(self.inputFields[0])
        pass


if __name__ == "__main__":
    m = Module()
    m.run()