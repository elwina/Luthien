import os
import uuid
from core.base.raster2Type import TYPE_Raster_Data
from core.typing.defineType import TYPE_Define_Config
from core.typing.ioType import TYPE_IO_Data
from osgeo import gdal, ogr, osr, gdalconst


def _config(new={}) -> TYPE_Define_Config:
    config = {"inFilePath": ""}
    config.update(new)
    return config


def raster2IO(ioData: TYPE_IO_Data) -> TYPE_IO_Data:
    from core.base.raster2 import RasterBase

    config = _config(ioData["config"])
    ins: RasterBase = ioData["ins"]
    data = TYPE_Raster_Data()

    if config["inFilePath"] != "":
        filepath = config["inFilePath"]
        src = gdal.Open(filepath, gdalconst.GA_ReadOnly)
        targetBand = src.GetRasterBand(1)
        array = targetBand.ReadAsArray()
        nodata = targetBand.GetNoDataValue()
        if nodata is not None:
            array[array == nodata] = -9999

        tempFile = os.path.join("temp", str(uuid.uuid4()) + ".tiff")
        gdalDriver = gdal.GetDriverByName("GTiff")
        dst = gdalDriver.CreateCopy(tempFile, src, 0)
        outband = dst.GetRasterBand(1)
        outband.WriteArray(array)
        outband.SetNoDataValue(-9999)
        outband.FlushCache()

        data.file = tempFile
        src = None
        dst = None

    ins.data = data
    ioData["newData"] = data
    return ioData
