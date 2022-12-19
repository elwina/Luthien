from typing import Dict, List, Literal, Any, Sequence
from typing_extensions import TypedDict, NotRequired

from core.typing.defineType import TYPE_Define
from core.typing.outputType import TYPE_A_Output_Action
from core.typing.recordType import TYPE_A_Record


class TYPE_A_Link_Input(TypedDict):
    into: str
    use: Literal["instance", "define"]
    instance: NotRequired[str]
    define: NotRequired[TYPE_Define]


class TYPE_Link_Declare(TypedDict):
    module: str
    timeInter: int
    input: Sequence[TYPE_A_Link_Input]
    output: Sequence[TYPE_A_Output_Action]
    recordInside: Sequence[TYPE_A_Record]
    record: Sequence[TYPE_A_Record]
