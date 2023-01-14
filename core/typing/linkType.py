from typing import Dict, List, Literal, Any, MutableSequence
from typing_extensions import TypedDict, NotRequired
from core.typing.defineType import TYPE_Define_Declare
from core.typing.outputType import TYPE_Output_Action_Declare
from core.typing.recordType import TYPE_Record_Declare


class TYPE_Input_Declare(TypedDict):
    into: str
    use: Literal["instance", "define"]
    instance: NotRequired[str]
    define: NotRequired[TYPE_Define_Declare]  # TODO 待开发


class TYPE_Link_Declare(TypedDict):
    module: str
    timeInter: int
    input: MutableSequence[TYPE_Input_Declare]
    output: MutableSequence[TYPE_Output_Action_Declare]
    recordInside: MutableSequence[TYPE_Record_Declare]
    record: MutableSequence[TYPE_Record_Declare]
