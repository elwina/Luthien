import os
import shutil
import uuid

from typing import Any, MutableMapping, Sequence
from core.base.base import BaseBase

from core.typing.ioType import TYPE_IO
from core.typing.recordType import TYPE_Recorder, TYPE_Recorder_TempEnv


class JsonBase(BaseBase):
    data: Any = {}

    def __init__(self, typeName: str):
        self.typeName = typeName
        super().__init__()

    def init(self):
        data = {}

    def define(self, method: TYPE_IO, config: MutableMapping[str, Any],
               data: Any):
        re = method({"config": config, "ins": self, "newData": data})

    def record(self, method: TYPE_Recorder, config: MutableMapping[str, Any],
               tempEnv: TYPE_Recorder_TempEnv):
        method({"config": config, "ins": self, "tempEnv": tempEnv})
