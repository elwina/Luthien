import os
import shutil
import uuid

from typing import Any, MutableMapping, Sequence
from core.base.base import BaseBase

from core.typing.ioType import TYPE_IO
from core.typing.recordType import TYPE_Recorder, TYPE_Recorder_TempEnv


class FileBase(BaseBase):
    fname: str = ""
    data: MutableMapping[str, str] = {}

    def __init__(self, typeName: str):
        self.typeName = typeName
        super().__init__()

    def init(self):
        fname = str(uuid.uuid4())
        self.fname = fname
        # 新建temp文件夹
        tempDir = os.path.join("temp", fname)
        os.mkdir(tempDir)

    def define(self, method: TYPE_IO, config: MutableMapping[str, Any],
               data: Any):
        config["fname"] = self.fname
        re = method({"config": config, "ins": self, "newData": data})

    def record(self, method: TYPE_Recorder, config: MutableMapping[str, Any],
               tempEnv: TYPE_Recorder_TempEnv):
        method({"config": config, "ins": self, "tempEnv": tempEnv})

    def getFile(self, name, dst):
        shutil.copy(self.data[name], dst)

    def getAFilePath(self, name: str):
        return self.data[name]

    def getFileNames(self) -> Sequence[str]:
        return list(self.data.keys())
