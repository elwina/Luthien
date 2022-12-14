from typing import Protocol, List, Dict, Type


class TYPE_Field(Protocol):
    typeName: str

    def __init__(self):
        pass


TYPE_FIRLD_LIST = Dict[str, Type[TYPE_Field]]
