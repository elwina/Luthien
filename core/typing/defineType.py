from typing import Any, Literal, MutableMapping, Sequence, TypedDict


class TYPE_Define_Declare(TypedDict):
    method: str
    config: MutableMapping[str, Any]
    data: Any


class TYPE_Init_Declare(TypedDict):
    use: Literal["define", "no", "copy"]
    define: TYPE_Define_Declare
    copy: str


TYPE_Define_Config = MutableMapping[str, Any]
