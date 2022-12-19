from typing import Any, Callable, MutableMapping, Sequence, TypeVar, TypedDict


class TYPE_A_Record(TypedDict):
    catch: str
    method: str
    config: MutableMapping


class TYPE_Recorder_Env(TypedDict):
    time: int
    pre: str


class TYPE_Recorder_Data(TypedDict):
    config: MutableMapping[str, Any]
    data: Any
    env: TYPE_Recorder_Env


TYPE_Recorder_Res = Sequence[str]

TYPE_Recorder = Callable[[TYPE_Recorder_Data], None]

TYPE_RECORDER_LIST = MutableMapping[str, TYPE_Recorder]
