import os
from typing import Any, MutableMapping, Sequence
import uuid
from core.base.base import BaseBase
from core.base.rasterType import TYPE_RASTER_DATA
from core.typing.ioType import TYPE_IO
from core.typing.recordType import TYPE_Recorder, TYPE_Recorder_Env, TYPE_Recorder_TempEnv


class RasterBase(BaseBase):
    '''基础类型:Raster,处理栅格'''
    '''data类型详见TYPE_RASTER_DATA'''
    data: TYPE_RASTER_DATA

    # 初始化函数
    def __init__(self, typeName: str):
        self.typeName = typeName
        super().__init__()

    def init(self):
        '''每个子类必须调用此函数'''
        initData = TYPE_RASTER_DATA(row=2,
                                    col=3,
                                    cellSize=100.0,
                                    nullData=-9999.0,
                                    xllCorner=0.0,
                                    yllCorner=0.0,
                                    radata=[[0., 0., 0.], [0., 0., 0.]])
        self.data = initData

    # 接口函数
    def define(self, method: TYPE_IO, config: MutableMapping[str, Any],
               data: Any):
        config["outRasterBase"] = True
        re = method({"config": config, "ins": self, "newData": data})

    def record(self, method: TYPE_Recorder, config: MutableMapping[str, Any],
               tempEnv: TYPE_Recorder_TempEnv):
        method({"config": config, "ins": self, "tempEnv": tempEnv})

    def defineFromAsciiFile(self, file: str):
        config = {"outRasterBase": True, "inDriver": "AAIGrid", "inFilePath": file}
        from core.io.txt2RasterIO import txt2RasterIO
        txt2RasterIO({"config": config, "ins": self, "newData": {}})

    def getTempFile(self):
        filepath = os.path.join("temp", str(uuid.uuid4()) + ".txt")
        from core.tools.raster2Txt import raster2Txt
        raster2Txt(self.data, filepath)
        return filepath

    def maskData(self,
                 maskRaster: TYPE_RASTER_DATA) -> Sequence[float | int] | None:
        '''掩膜,要求一样多的格子'''
        re = []
        data = self.data
        novalue = data.nullData
        rdata = data.radata

        maskNovalue = maskRaster.nullData
        maskData = maskRaster.radata

        if data.row != maskRaster.row or data.col != maskRaster.col:
            return None

        for i in range(data.row):
            for j in range(data.col):
                if rdata[i][j] != novalue and maskData[i][j] != maskNovalue:
                    re.append(rdata[i][j])

        return re

    def timesANum(self, num: float | int):
        '''乘以一个数'''
        data = self.data
        novalue = data.nullData
        rdata = data.radata

        for i in range(data.row):
            for j in range(data.col):
                if rdata[i][j] != novalue:
                    rdata[i][j] *= num