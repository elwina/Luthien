from typing import Any, MutableMapping, Protocol, List, Dict, Type, TypedDict

from core.typing.defineType import TYPE_Declare_Define


class TYPE_Field(Protocol):
    typeName: str
    data: Any

    def __init__(self):
        pass

    def define(self, methodName: str, config: MutableMapping[str, Any],
               data: Any) -> None:
        pass


class Type_Instance_Declare(TypedDict):
    field: str
    init: TYPE_Declare_Define

TYPE_Instance = TYPE_Field

TYPE_FIELD_LIST = MutableMapping[str, Type[TYPE_Field]]
