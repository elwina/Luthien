from typing import Any, MutableMapping
from typing_extensions import TypedDict


class TYPE_Output_Action_Declare(TypedDict):
    catch: str
    put: str
    longTime: bool  # true 为长时间输出，false 为一次性输出
    timeInter: int  # TODO 待开发


TYPE_Output_Information = MutableMapping[str, MutableMapping[str, Any]]

TYPE_Putout = MutableMapping[str, MutableMapping[int, Any]]
