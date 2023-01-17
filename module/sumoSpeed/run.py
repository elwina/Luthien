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
from core.base.json import JsonBase
from core.typing.fieldType import TYPE_Instance
from core.typing.outputType import TYPE_Putout

from module.sumoSpeed.information import MODULE_ROOT
from core.tools.vector2raster import vector2raster

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

    rasterPath = os.path.join(tempDir, "autowater.txt")
    shutil.copy(water.getTempFile(), rasterPath)
    outRasterPath = os.path.join(tempDir, "autoroadinraster.txt")

    streets = road.getAllStreets()

    def getAMeanWater():
        meanOneWater: MutableMapping[str, float] = {}
        for index, street in enumerate(streets):
            roadPath = os.path.join(tempDir, "autoroad%d.geojson" % index)
            shutil.copy(road.getAStreet(street).getTempFile(), roadPath)

            vector2raster(roadPath, rasterPath, outRasterPath)
            roadRaster = RasterBase("road")
            roadRaster.init()
            roadRaster.defineFromAsciiFile(outRasterPath)

            roadRData = roadRaster.data
            waterinroad = water.maskData(roadRData)
            if waterinroad is not None:
                meanOneWater[street] = listMean(waterinroad)
            else:
                meanOneWater[street] = -1
        return meanOneWater

    meanWaterList: dict[str, list[float]] = dict(
        zip(streets, [[] for _ in range(len(streets))]))
    for time, ins in water.iTM.geneKeyFrame():
        meanAWater = getAMeanWater()
        for street in streets:
            if meanAWater[street] != -1:
                meanWaterList[street].append(meanAWater[street])

    meanWater: MutableMapping[str, float] = dict(
        map(lambda x: (x[0], listMean(x[1])), meanWaterList.items()))

    streetMeanWaterJson = JsonBase("streetMeanWater")
    streetMeanWaterJson.init()
    streetMeanWaterJson.data = meanWater
    putout({"streetMeanWaterJson": {0: streetMeanWaterJson}})


def listMean(list: Sequence):
    return sum(list) / len(list)
