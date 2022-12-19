from typing import Dict, List, Literal, Any, Sequence
from typing_extensions import TypedDict, NotRequired

from core.typing.defineType import TYPE_Define


class TYPE_A_Link_Input(TypedDict):
    into: str
    use: Literal["instance", "define"]
    instance: NotRequired[str]
    define: NotRequired[TYPE_Define]


class TYPE_Link_Declare(TypedDict):
    module: str
    timeInter:int
    input: Sequence[TYPE_A_Link_Input]
    output: Any
