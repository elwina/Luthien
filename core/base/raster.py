from typing import Any, MutableMapping, Sequence, TypedDict

from config.register import IO_LIST


class TYPE_RASTER_DATA(TypedDict):
    row: int
    col: int
    cellSize: float
    nullData: float
    xllCorner: float
    yllCorner: float
    radata: Sequence[Sequence[float]]


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
