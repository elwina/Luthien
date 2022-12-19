from typing import Sequence
from core.typing.inputType import TYPE_Indata, TYPE_Information
from core.mod.inputManager import inputManager

from core.typing.moduleType import TYPE_Module


class ModuleTemplate(TYPE_Module):
    inMr: inputManager

    def __init__(self, name, instancesInf: TYPE_Information):
        self.name = name
        self.inMr = inputManager()
        self.inMr.init(instancesInf)

    def prepareData(self, indata: TYPE_Indata):
        self.inMr.receiveData(indata)
