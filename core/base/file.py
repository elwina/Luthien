import os
import shutil
import uuid

from typing import Any, MutableMapping, Sequence

from core.typing.ioType import TYPE_IO
from core.typing.recordType import TYPE_Recorder, TYPE_Recorder_TempEnv


class FileBase:
    fname: str = ""
    data: MutableMapping[str, str] = {}

    def __init__(self, typeName: str):
        self.typeName = typeName

    def init(self):
        fname = str(uuid.uuid4())
        self.fname = fname
        # 新建temp文件夹
        tempDir = os.path.join("temp", fname)
        os.mkdir(tempDir)

    def define(self, method: TYPE_IO, config: MutableMapping[str, Any],
               data: Any):
        config["fname"] = self.fname
        re = method({"config": config, "oldData": self.data, "newData": data})
        self.data = re["newData"]
        print(self.data)

    def record(self, method: TYPE_Recorder, config: MutableMapping[str, Any],
               tempEnv: TYPE_Recorder_TempEnv):
        method({"config": config, "data": self.data, "tempEnv": tempEnv})

    def getFile(self, name, dst):
        shutil.copy(self.data[name], dst)

    def getFileNames(self) -> Sequence[str]:
        return list(self.data.keys())
