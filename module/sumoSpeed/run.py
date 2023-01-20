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
    waterTimes = water.iTM.getKeyframe()

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

    meanWaterList: dict[str, list[float | int]] = dict(
        zip(streets, [[] for _ in range(len(streets))]))
    for time, ins in water.iTM.geneKeyFrame():
        meanAWater = getAMeanWater()
        for street in streets:
            meanWaterList[street].append(meanAWater[street])

    meanWater: MutableMapping[str, float] = dict(
        map(lambda x: (x[0], listMean(list(filter(lambda y: y != -1, x[1])))),
            meanWaterList.items()))

    streetMeanWaterJson = JsonBase("streetMeanWater")
    streetMeanWaterJson.init()
    streetMeanWaterJson.data = meanWater
    putout({"streetMeanWaterJson": {0: streetMeanWaterJson}})

    # 将积水与路况挂钩
    # 使用会议论文拟合公式
    timeRoadSpeed: MutableMapping[int, MutableMapping[str, Any]] = {}
    for ind in range(water.iTM.getKeyframe().__len__()):
        time = waterTimes[ind]
        timeRoadSpeed[time] = {}
        for street in streets:
            depth = meanWaterList[street][ind]
            if depth != -1:
                v0 = road.getAStreet(street).data.objects[0].properties.get(
                    "speed", 30)
                if v0 == 0: v0 = 30
                speed, change = newSpeed(v0, depth)
                timeRoadSpeed[time][street] = {
                    "speed": speed,
                    "change": change
                }
    timeRoadSpeedJson = JsonBase("timeRoadSpeed")
    timeRoadSpeedJson.init()
    timeRoadSpeedJson.data = timeRoadSpeed
    putout({"timeRoadSpeedJson": {0: timeRoadSpeedJson}})


def newSpeed(v0: float, depth: float):
    x = depth
    a = 7.5
    b = 3
    v = 0.5 * v0 * math.tanh((-x + a) / b) + 0.5 * v0
    return v, (v - v0) / v0


def listMean(list: Sequence):
    return sum(list) / len(list)
