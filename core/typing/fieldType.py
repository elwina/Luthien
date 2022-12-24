from typing import Any, MutableMapping, Protocol, List, Dict, Type, TypedDict

from core.typing.defineType import TYPE_Declare_Define
from core.typing.ioType import TYPE_IO
from core.typing.recordType import TYPE_Recorder, TYPE_Recorder_Env, TYPE_Recorder_TempEnv


class TYPE_Field(Protocol):
    typeName: str
    data: Any

    def __init__(self):
        pass

    def define(self, methodIO: TYPE_IO, config: MutableMapping[str, Any],
               data: Any) -> None:
        pass

    def record(self, methodRecorder: TYPE_Recorder,
               config: MutableMapping[str,
                                      Any], tempEnv: TYPE_Recorder_TempEnv):
        pass


class Type_Instance_Declare(TypedDict):
    name: str
    field: str
    init: TYPE_Declare_Define
    record: str


TYPE_Instance = TYPE_Field

TYPE_FIELD_LIST = MutableMapping[str, Type[TYPE_Field]]
