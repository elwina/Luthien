from typing import Any, MutableMapping
from typing_extensions import TypedDict


class TYPE_Output_Action_Declare(TypedDict):
    catch: str
    put: str


TYPE_Output_Information = MutableMapping[str, MutableMapping[str, Any]]

TYPE_Putout = MutableMapping[str, MutableMapping[int, Any]]
