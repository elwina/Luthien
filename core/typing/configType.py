from typing import MutableMapping, Sequence, TypedDict

from core.typing.defineType import TYPE_Declare_Define
from core.typing.linkType import TYPE_Link_Declare


class Type_Instance_Declare(TypedDict):
    field: str
    init: TYPE_Declare_Define


class Type_Config_Json(TypedDict):
    version: int
    instance: MutableMapping[str, Type_Instance_Declare]
    link: Sequence[TYPE_Link_Declare]
