from typing import Any, Callable, MutableMapping, Sequence, TypeVar, TypedDict


class TYPE_Record_Declare(TypedDict):
    catch: str
    method: str
    config: MutableMapping
    time: str


class TYPE_Recorder_TempEnv(TypedDict):
    insName: str
    ifModule: bool
    linkDes: str


class TYPE_Recorder_Env(TypedDict):
    insName: str
    fileType: str
    ifModule: bool
    linkDes: str
    recNum: int


class TYPE_Recorder_Data(TypedDict):
    config: MutableMapping[str, Any]
    ins: Any
    tempEnv: TYPE_Recorder_TempEnv


TYPE_Recorder = Callable[[TYPE_Recorder_Data], None]

TYPE_RECORDER_LIST = MutableMapping[str, TYPE_Recorder]
