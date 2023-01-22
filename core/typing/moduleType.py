from abc import abstractmethod
from typing import ClassVar, Protocol, List, Dict, Type, TypedDict
from core.mod.inputManager import inputManager
from core.mod.outputManager import outputManager

from core.typing.fieldType import TYPE_Field
from core.typing.inputType import TYPE_Indata, TYPE_Information
from core.typing.outputType import TYPE_Output_Information


class TYPE_Module(Protocol):
    inMr: inputManager
    outMr: outputManager

    moduleName: str
    inInf: TYPE_Information
    outInf: TYPE_Output_Information

    def prepareData(self, indata: TYPE_Indata) -> None:
        pass

    def run(self) -> None:
        pass


TYPE_MODULE_LIST = dict[str, Type[TYPE_Module]]
