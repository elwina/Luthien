from typing import MutableMapping, Sequence, TypedDict

from core.typing.fieldType import Type_Instance_Declare
from core.typing.linkType import TYPE_Link_Declare


class TYPE_Basic_Config(TypedDict):
    timestep: int
    timeUnit: str
    timeEpoch: int
    outputPath: str


class Type_Config_Json(TypedDict):
    version: int
    basic: TYPE_Basic_Config
    instance: Sequence[Type_Instance_Declare]
    link: Sequence[TYPE_Link_Declare]
