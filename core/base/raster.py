from typing import Any, MutableMapping, Sequence, TypedDict

from config.register import IO_LIST, RECORDER_LIST
from core.base.rasterType import TYPE_RASTER_DATA
from core.typing.recordType import TYPE_Recorder_Env, TYPE_Recorder_TempEnv


class RasterBase:
    data: TYPE_RASTER_DATA

    def __init__(self, typeName: str):
        self.typeName = typeName

    # 初始化与默认值
    def init(self):
        initData: TYPE_RASTER_DATA = {
            "row": 2,
            "col": 3,
            "cellSize": 100.0,
            "nullData": -9999.0,
            "xllCorner": 0.0,
            "yllCorner": 0.0,
            "radata": [[0., 0., 0.], [0., 0., 0.]]
        }
        self.data = initData

    def define(self, methodName: str, config: MutableMapping[str, Any],
               data: Any):
        method = IO_LIST[methodName]
        config["outRasterBase"] = True
        re = method({"config": config, "oldData": self.data, "newData": data})
        self.data = re["newData"]

    def record(self, methodName: str, config: MutableMapping[str, Any],
               tempEnv: TYPE_Recorder_TempEnv):
        method = RECORDER_LIST[methodName]
        method({"config": config, "data": self.data, "tempEnv": tempEnv})
