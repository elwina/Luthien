from typing import Any, MutableMapping
import pandas as pd
from core.base.base import BaseBase
from core.typing.fieldType import TYPE_Field, TYPE_Instance

from core.base.file import FileBase
from core.typing.ioType import TYPE_IO
from core.typing.recordType import TYPE_Recorder, TYPE_Recorder_TempEnv


class TableBase(BaseBase):
    """内置Field:csv"""

    data: pd.DataFrame

    def __init__(self):
        super().__init__()

    def init(self):
        self.data = pd.DataFrame()

    def define(self, method: TYPE_IO, config: MutableMapping[str, Any], data: Any):
        method({"config": config, "ins": self, "newData": data})

    def record(
        self,
        method: TYPE_Recorder,
        config: MutableMapping[str, Any],
        tempEnv: TYPE_Recorder_TempEnv,
    ):
        method({"config": config, "ins": self, "tempEnv": tempEnv})

    def setPandasData(self, data):
        self.data = data

    def toCSVFile(self, path: str):
        self.data.to_csv(path, index=False)
