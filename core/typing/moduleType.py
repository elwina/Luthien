from abc import abstractmethod
from typing import ClassVar, Protocol, List, Dict, Type
from core.mod.inputManager import inputManager

from core.typing.fieldType import TYPE_Field
from core.typing.inputType import TYPE_Indata


class TYPE_Module(Protocol):
    inMr: inputManager

    def prepareData(self, indata: TYPE_Indata) -> None:
        pass

    def run(self) -> None:
        pass


TYPE_MODULE_LIST = dict[str, Type[TYPE_Module]]
