from typing import Any, MutableMapping
from typing_extensions import TypedDict


class TYPE_A_Output_Action(TypedDict):
    catch: str
    put: str
    timeInter: int


TYPE_Output_Information = MutableMapping[str, MutableMapping[str, Any]]

TYPE_Putout = MutableMapping[str, MutableMapping[int, Any]]
