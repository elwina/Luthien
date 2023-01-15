from typing import Any, Callable, MutableMapping, TypeVar, TypedDict


class TYPE_IO_Data(TypedDict):
    config: MutableMapping[str, Any]
    ins: Any
    newData: Any


TYPE_IO = Callable[[TYPE_IO_Data], TYPE_IO_Data]
TYPE_IO_LIST = MutableMapping[str, TYPE_IO]
