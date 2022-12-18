from abc import abstractmethod
from typing import ClassVar, Protocol, List, Dict, Type

from core.typing.fieldType import TYPE_Field


class TYPE_Module(Protocol):
    # inputFieldsNames: list[str]

    def prepareData(self, list: list[TYPE_Field]) -> None:
        pass

    def run(self) -> None:
        pass


TYPE_MODULE_LIST = dict[str, Type[TYPE_Module]]
