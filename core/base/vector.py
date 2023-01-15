from typing import Any, MutableMapping
from core.typing.ioType import TYPE_IO, TYPE_IO_Data
from core.typing.recordType import TYPE_Recorder, TYPE_Recorder_Env, TYPE_Recorder_TempEnv
from core.base.vectorType import TYPE_VECTOR_DATA, TYPE_VECTOR_TYPE


class VectorBase:
    data: TYPE_VECTOR_DATA

    def __init__(self, typeName: str):
        self.typeName = typeName

    def init(self, type: TYPE_VECTOR_TYPE):
        self.data = {"type": type, "objects": []}

    # 接口函数
    def define(self, method: TYPE_IO, config: MutableMapping[str, Any],
               data: Any):
        re = method({"config": config, "ins": self, "newData": data})
