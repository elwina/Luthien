from typing import Any, MutableMapping, Protocol, List, Dict, Type


class TYPE_Field(Protocol):
    typeName: str

    def __init__(self):
        pass

    def define(self, methodName: str, config: MutableMapping[str, Any],
               data: Any) -> None:
        pass


TYPE_Instance = TYPE_Field

TYPE_FIELD_LIST = MutableMapping[str, Type[TYPE_Field]]
