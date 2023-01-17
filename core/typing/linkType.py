from typing import Dict, List, Literal, Any, Sequence
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
    time: str
    input: Sequence[TYPE_Input_Declare]
    output: Sequence[TYPE_Output_Action_Declare]
    recordInside: Sequence[TYPE_Record_Declare]
    record: Sequence[TYPE_Record_Declare]
