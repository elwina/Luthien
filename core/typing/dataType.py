from typing import Any, MutableMapping, Sequence, TypedDict


class TYPE_A_Data(TypedDict):
    method: str
    config: MutableMapping[str, Any]
    data: Any


TYPE_DATA_JSON = MutableMapping[str,TYPE_A_Data]
