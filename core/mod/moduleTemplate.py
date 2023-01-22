import string
from core.typing.moduleType import TYPE_Module
from core.typing.outputType import TYPE_Output_Information
from core.typing.inputType import TYPE_Indata, TYPE_Information

from core.mod.inputManager import inputManager
from core.mod.outputManager import outputManager


class ModuleTemplate(TYPE_Module):
    inMr: inputManager
    outMr: outputManager

    moduleName: str
    inInf: TYPE_Information
    outInf: TYPE_Output_Information

    def __init__(self, name, instancesInf: TYPE_Information,
                 outInstancesInf: TYPE_Output_Information):
        self.name = name
        self.inMr = inputManager()
        self.inMr.init(instancesInf)
        self.outMr = outputManager()
        self.outMr.init(outInstancesInf)

        self.moduleName = name
        self.inInf = instancesInf
        self.outInf = outInstancesInf

    def prepareData(self, indata: TYPE_Indata):
        self.inMr.receiveData(indata)
