from typing import Any, MutableMapping, Protocol, List, Dict, Type, TypeVar, TypedDict
from core.typing.defineType import TYPE_Init_Declare
from core.typing.ioType import TYPE_IO
from core.typing.recordType import TYPE_Recorder, TYPE_Recorder_Env, TYPE_Recorder_TempEnv

class TYPE_Field(Protocol):
    '''Field与Instance的类型定义'''

    typeName: str
    '''Field名,备用'''

    data: Any
    '''存储所有数据'''

    from core.insTimeManager import InsTimeManager
    iTM: InsTimeManager

    def __init__(self):
        pass

    def define(self, methodIO: TYPE_IO, config: MutableMapping[str, Any],
               data: Any) -> None:
        '''重要定义函数'''
        pass

    def record(self, methodRecorder: TYPE_Recorder,
               config: MutableMapping[str,
                                      Any], tempEnv: TYPE_Recorder_TempEnv):
        '''重要记录函数'''
        pass


class Type_Instance_Declare(TypedDict):
    name: str
    field: str
    init: TYPE_Init_Declare
    record: str


TYPE_Instance = TYPE_Field

TYPE_FIELD_LIST = MutableMapping[str, Type[TYPE_Field]]
