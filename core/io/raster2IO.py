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


def raster2IO(ioData: TYPE_IO_Data) -> int:
    from core.base.raster2 import RasterBase

    config = _config(ioData["config"])
    ins: RasterBase = ioData["ins"]
    data = TYPE_Raster_Data()

    if config["inFilePath"] != "":
        filepath = config["inFilePath"]
        ins.setImportFromFile(filepath)
        return 0
    else:
        return -1
