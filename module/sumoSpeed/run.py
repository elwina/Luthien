import math
import os
from pathlib import Path
import shutil
import subprocess
import platform

from typing import Any, Callable, MutableMapping, Sequence, cast
import uuid
from core.base.listConf import ListConfBase
from core.base.raster import RasterBase
from core.typing.fieldType import TYPE_Instance
from core.typing.outputType import TYPE_Putout

from module.sumoSpeed.information import MODULE_ROOT

from loguru import logger


def sumoSpeedRun(putout: Callable[[TYPE_Putout], None],
                 instances: MutableMapping[str, TYPE_Instance],
                 optList: Sequence[str]):
    logger.debug("Module sumoSpeed Run,optList:{opt}.", opt=",".join(optList))

    # 从instances中获取需要的实例
    from module.sumoSpeed.field.uniField import UniField
    from core.field.roadField import RoadField
    from core.field.waterField import WaterField
    sumoSpeedUni = cast(UniField, instances["sumoSpeedUni"])
    road = cast(RoadField, instances["road"])
    water = cast(WaterField, instances["water"])

    # 新建temp文件夹
    tempDir = os.path.join(MODULE_ROOT, "temp")
    shutil.rmtree(tempDir, ignore_errors=True)
    os.mkdir(tempDir)

    roadPath = os.path.join(tempDir, "autoroad.geojson")
    rasterPath = os.path.join(tempDir, "autowater.txt")
    shutil.copy(road.getTempFile(), roadPath)
    shutil.copy(water.getTempFile(), rasterPath)
    outRasterPath = os.path.join(tempDir, "autoroadinraster.txt")
    from core.tools.vector2raster import vector2raster
    vector2raster(roadPath, rasterPath, outRasterPath)
    from core.base.raster import RasterBase
    roadRaster = RasterBase("road")
    roadRaster.init()
    roadRaster.defineFromAsciiFile(outRasterPath)
    roadRData = roadRaster.data
    waterRData = water.data
    roadRData
