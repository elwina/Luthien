from typing import Any, Literal, MutableMapping, MutableSequence, TypedDict


class TYPE_Define_Declare(TypedDict):
    method: str
    config: MutableMapping[str, Any]
    data: Any


class TYPE_Init_Declare(TypedDict):
    use: Literal["define", "no", "copy"]
    define: TYPE_Define_Declare