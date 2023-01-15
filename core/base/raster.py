from typing import Any, MutableMapping
from core.base.rasterType import TYPE_RASTER_DATA
from core.typing.ioType import TYPE_IO
from core.typing.recordType import TYPE_Recorder, TYPE_Recorder_Env, TYPE_Recorder_TempEnv


class RasterBase:
    '''基础类型:Raster,处理栅格'''
    '''data类型详见TYPE_RASTER_DATA'''
    data: TYPE_RASTER_DATA

    # 初始化函数
    def __init__(self, typeName: str):
        self.typeName = typeName

        def asd():
            return "1"

    def init(self):
        '''每个子类必须调用此函数'''
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

    # 接口函数
    def define(self, method: TYPE_IO, config: MutableMapping[str, Any],
               data: Any):
        config["outRasterBase"] = True
        re = method({"config": config, "ins": self, "newData": data})

    def record(self, method: TYPE_Recorder, config: MutableMapping[str, Any],
               tempEnv: TYPE_Recorder_TempEnv):
        method({"config": config, "ins": self, "tempEnv": tempEnv})

    def defineFromAsciiFile(self,file:str):
        config={
            "outRasterBase":True,
            "inFile":True,
            "inFilePath": file
        }
        from core.io.txt2RasterIO import txt2RasterIO
        txt2RasterIO({"config": config, "ins": self, "newData": {}})
