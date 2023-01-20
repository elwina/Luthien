from dataclasses import dataclass
from typing import Literal, MutableMapping, Optional
from typing_extensions import Required, TypedDict

from core.typing.fieldType import TYPE_Instance


class _TYPE_Indata_Declare(TypedDict):
    method: Literal["in"]
    instance: TYPE_Instance


TYPE_Indata = MutableMapping[str, _TYPE_Indata_Declare]


class _TYPE_A_Information(TypedDict):
    required: bool


TYPE_Information = MutableMapping[str, _TYPE_A_Information]
