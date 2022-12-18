from typing import Any, Literal, MutableMapping, Sequence, TypedDict


class TYPE_Define(TypedDict):
    method: str
    config: MutableMapping[str, Any]
    data: Any


class TYPE_Declare_Define(TypedDict):
    use: Literal["define", "no", "copy"]
    define: TYPE_Define