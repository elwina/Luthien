import os
import uuid
import numpy as np
from osgeo import gdal, ogr, osr, gdalconst


from typing import Any
from core.base.base import BaseBase
from core.base.raster2Type import TYPE_Raster_Data
from core.typing.defineType import TYPE_Define_Config
from core.typing.ioType import TYPE_IO
from core.typing.recordType import (
    TYPE_Record_Config,
    TYPE_Recorder,
    TYPE_Recorder_TempEnv,
)


class RasterBase(BaseBase):
    """基础类型:Raster,处理栅格"""

    data: TYPE_Raster_Data

    def __init__(self, typeName: str):
        super().__init__()

    def init(self):
        """每个子类必须调用此函数"""
        initData = ""
        self.data.file = initData

    def define(self, method: TYPE_IO, config: TYPE_Define_Config, data: Any):
        method({"config": config, "ins": self, "newData": data})

    def record(
        self,
        method: TYPE_Recorder,
        config: TYPE_Record_Config,
        tempEnv: TYPE_Recorder_TempEnv,
    ):
        method({"config": config, "ins": self, "tempEnv": tempEnv})

    def setRaster(self, file: str):
        """设置栅格"""
        self.data.file = file

    def getRaster(self):
        """获取栅格"""
        return self.data.file

    def raster2array(self, bandNum=1):
        """栅格转数组"""
        raster = gdal.Open(self.data.file)
        band = raster.GetRasterBand(bandNum)
        array = band.ReadAsArray()
        array = np.array(array)
        nodata = band.GetNoDataValue()
        return array, nodata

    def array2raster(self, newRasterfn, array, nodata=None):
        """数组转栅格"""
        raster = gdal.Open(self.data.file)
        geotransform = raster.GetGeoTransform()
        originX = geotransform[0]
        originY = geotransform[3]
        pixelWidth = geotransform[1]
        pixelHeight = geotransform[5]
        cols = raster.RasterXSize
        rows = raster.RasterYSize

        driver = gdal.GetDriverByName("GTiff")
        outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float64)
        outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
        outband = outRaster.GetRasterBand(1)
        outband.WriteArray(array)
        if nodata is not None:
            outband.SetNoDataValue(nodata)
        outband.FlushCache()

        # outRasterSRS = osr.SpatialReference()
        # outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
        # outRaster.SetProjection(outRasterSRS.ExportToWkt())

    def alterTimeANum(self, num: float | int):
        """所有栅格乘以一个数"""
        array, nodata = self.raster2array()
        array[array != nodata] = array[array != nodata] * num
        tempFile = os.path.join("temp", str(uuid.uuid4()) + ".tiff")
        self.array2raster(tempFile, array, nodata)
        self.data.file = tempFile

    def getMaskLinearData(self, maskRaster: TYPE_Raster_Data):
        """获取掩膜线性数据"""
        array, nodata = self.raster2array()
        array[array == nodata] = 0
        tempIns = RasterBase("temp")
        tempIns.setRaster(maskRaster.file)
        maskArray, maskNodata = tempIns.raster2array()
        if array.shape != maskArray.shape:
            raise Exception("掩膜与栅格大小不一致")
        array[maskArray == maskNodata] = 0
        re = array[array != 0]
        return re


r = RasterBase("r")
from core.io.raster2IO import raster2IO

r.define(raster2IO, {"inFilePath": "data/cz/4336sq_utm.tif"}, None)
r.alterTimeANum(10)

print(0)
