from typing import Literal, MutableMapping, Optional, TypedDict
from typing_extensions import NotRequired

from core.typing.fieldType import TYPE_Instance


class _TYPE_A_Indata(TypedDict):
    method: Literal["in"]
    instance: NotRequired[TYPE_Instance]


TYPE_Indata = MutableMapping[str, _TYPE_A_Indata]


class _TYPE_A_Information(TypedDict):
    required: bool


TYPE_Information = MutableMapping[str, _TYPE_A_Information]
