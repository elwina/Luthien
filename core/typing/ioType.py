from typing import Any, Callable, MutableMapping, TypeVar, TypedDict


class TYPE_IO_DATA(TypedDict):
    config: MutableMapping[str, Any]
    oldData: Any
    newData: Any


TYPE_IO = Callable[[TYPE_IO_DATA], TYPE_IO_DATA]
TYPE_IO_LIST = MutableMapping[str, TYPE_IO]
