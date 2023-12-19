from copy import deepcopy
import math
import os
from pathlib import Path
import shutil
import subprocess
import platform
import xml.dom.minidom

from typing import Any, Callable, MutableMapping, Sequence, cast
from core.base.listConf import ListConfBase
from core.base.raster2 import RasterBase
from core.base.json import JsonBase
from core.base.vectorType import VectorData
from core.field.tempFileField import TempFileField
from core.io.fileListIO import fileListIO
from core.typing.fieldType import TYPE_Instance
from core.typing.outputType import TYPE_Putout

from module.sumoSpeed.information import MODULE_ROOT
from core.tools.vector2raster import vector2raster

from core.envGlobal import envGlobal as eGl
from loguru import logger


def sumoSpeedRun(
    putout: Callable[[TYPE_Putout], None],
    instances: MutableMapping[str, TYPE_Instance],
    optList: Sequence[str],
):
    logger.debug("Module sumoSpeed Run,optList:{opt}.", opt=",".join(optList))

    # 从instances中获取需要的实例
    from module.sumoSpeed.field.uniField import UniField
    from core.field.roadField import RoadField
    from core.field.waterField import WaterField

    uni = cast(UniField, instances["sumoSpeedUni"])
    sroad = cast(RoadField, instances["edgeRoad"])
    water = cast(WaterField, instances["water"])

    road = None
    if "road" in instances:
        road = cast(RoadField, instances["road"])

    timenow = eGl.epoch

    # 新建temp文件夹
    tempDir = os.path.join(MODULE_ROOT, "temp")
    shutil.rmtree(tempDir, ignore_errors=True)
    os.mkdir(tempDir)

    # water为模板栅格
    rasterPath = water.getRaster()
    outRasterPath = os.path.join(tempDir, "autoroadinraster.txt")

    # 计算每个edge的积水深度
    allEdgeid = sroad.getAllAProp("id")
    edgeWater: MutableMapping[int, MutableMapping[str, Any]] = {}
    for time, ins in water.iTM.geneKeyFrame():
        edgeWater[time] = {}
        for edgeid in allEdgeid:
            edgePath = os.path.join(tempDir, "autoedge%s.geojson" % edgeid)
            shutil.copy(sroad.getInsByOneProp("id", edgeid).getTempFile(), edgePath)

            outRasterPath = os.path.join(tempDir, "autoedgeinraster%s.tif" % edgeid)
            vector2raster(edgePath, rasterPath, outRasterPath)
            edgeRaster = RasterBase("edgeRoad")
            edgeRaster.init()
            edgeRaster.setRaster(outRasterPath)
            edgeRData = edgeRaster.data
            waterInEdge = water.getMaskLinearData(edgeRData)
            if waterInEdge is not None:
                edgeWater[time][edgeid] = listMean(waterInEdge)
            else:
                edgeWater[time][edgeid] = -1

    # Output1 edgeWaterJson 该时间每个edge的积水深度
    edgeWaterJson = JsonBase("edgeWater")
    edgeWaterJson.init()
    for time in edgeWater:
        edgeWaterJson.data = edgeWater[time]
        putout({"edgeWaterJson": {time - timenow: edgeWaterJson}})

    # Output3 edgeSpeedJson 该时间每个edge的速度
    edgeSpeed: MutableMapping[int, MutableMapping[str, dict]] = {}

    # Output2 sroad 更新水深，根据速度公式计算每个edge的速度
    newSroad = deepcopy(sroad)
    for time in edgeWater:
        data: VectorData = newSroad.iTM.getTimeIns(time).data
        edgeSpeed[time] = {}
        for obj in data.objects:
            edgeid: str = obj.properties["id"]
            depth = edgeWater[time][edgeid]
            if depth != -1:
                obj.properties["water_depth"] = depth

                # 核心速度公式区域
                v0 = obj.properties.get("ospeed", 30)
                if v0 == 0:
                    v0 = 30
                speed, change = newSpeed(v0, depth)

                obj.properties["speed"] = speed
                obj.properties["change"] = change

                edgeSpeed[time][edgeid] = {}
                edgeSpeed[time][edgeid]["speed"] = speed
                edgeSpeed[time][edgeid]["change"] = change
        newSroad.data = data
        putout({"sroad": {time - timenow: newSroad}})

    # Output3 edgeSpeedJson 该时间每个edge的速度
    edgeSpeedJson = JsonBase("edgeSpeed")
    edgeSpeedJson.init()
    for time in edgeSpeed:
        edgeSpeedJson.data = edgeSpeed[time]
        putout({"edgeSpeedJson": {time - timenow: edgeSpeedJson}})

    # Output7 vssAddFile
    vssXml = xml.dom.minidom.Document()
    vssRoot = vssXml.createElement("additional")
    for edgeid in allEdgeid:
        vssEdge = vssXml.createElement("variableSpeedSign")
        vssEdge.setAttribute("id", "vss" + edgeid)
        props = sroad.getObjByOneProp("id", edgeid)
        if props is not None and "lanes" in props.properties:
            vssEdge.setAttribute("lanes", " ".join(props.properties["lanes"]))

            from core.utils.timePeriod import timeStepSeconds

            tss = timeStepSeconds()
            for time in edgeSpeed:
                timeSeconds = time * tss
                vssEdgeTime = vssXml.createElement("step")
                vssEdgeTime.setAttribute("time", str(timeSeconds + 25200))
                vssEdgeTime.setAttribute("speed", str(edgeSpeed[time][edgeid]["speed"]))
                vssEdge.appendChild(vssEdgeTime)
        vssRoot.appendChild(vssEdge)

    vssXml.appendChild(vssRoot)
    vssPath = os.path.join(tempDir, "vss.add.xml")
    with open(vssPath, "w") as f:
        vssXml.writexml(f, indent="", addindent="\t", newl="\n")
    vssAddFile = TempFileField()
    vssAddFile.init()
    vssAddFile.define(fileListIO, {}, {"vss": vssPath})
    putout({"vssAddFile": {0: vssAddFile}})

    if road is not None and uni.getOne("ifStreet") == 1:
        # 按街道进行平均计算
        streets = road.getAllStreets()
        waterTimes = water.iTM.getKeyframe()

        # {街道:值}
        def getAMeanWater() -> dict[str, float]:
            meanOneWater: MutableMapping[str, float] = {}
            for index, street in enumerate(streets):
                roadPath = os.path.join(tempDir, "autoroad%d.geojson" % index)
                shutil.copy(road.getAStreet(street).getTempFile(), roadPath)

                outRasterPath = os.path.join(tempDir, "autoroadinraster%s.tif" % street)
                vector2raster(roadPath, rasterPath, outRasterPath)
                roadRaster = RasterBase("road")
                roadRaster.init()
                roadRaster.setRaster(outRasterPath)

                roadRData = roadRaster.data
                waterinroad = water.getMaskLinearData(roadRData)
                if waterinroad is not None:
                    meanOneWater[street] = listMean(waterinroad)
                else:
                    meanOneWater[street] = -1
            return meanOneWater

        streetWater: MutableMapping[int, MutableMapping[str, float]] = {}
        for time, ins in water.iTM.geneKeyFrame():
            meanAWater = getAMeanWater()
            streetWater[time] = meanAWater

        # Output4 streetWaterJson 该时间每个街道的积水深度
        streetWaterJson = JsonBase("streetWaterJson")
        streetWaterJson.init()
        for time in streetWater:
            streetWaterJson.data = streetWater[time]
            putout({"streetWaterJson": {time - timenow: streetWaterJson}})

        # Output5 road 更新水深，根据速度公式计算每个street的速度
        timeRoadSpeed: MutableMapping[int, MutableMapping[str, dict]] = {}
        newRoad = deepcopy(road)
        for time in waterTimes:
            newRoad.iTM.jumpTime(time)
            timeRoadSpeed[time] = {}
            for street in streets:
                depth = streetWater[time][street]
                if depth != -1:
                    props = newRoad.getAStreet(street).data.objects[0].properties
                    props["water_depth"] = depth

                    v0 = props.get("speed", 30)

                    # 核心速度公式区域
                    if v0 == 0:
                        v0 = 30
                    speed, change = newSpeed(v0, depth)

                    props["speed"] = speed
                    props["change"] = change
                    timeRoadSpeed[time][street] = {
                        "depth": depth,
                        "speed": speed,
                        "change": change,
                    }
            putout({"road": {time - timenow: newRoad}})

        # Output6 streetSpeedJson 该时间每个街道的速度
        streetSpeedJson = JsonBase("streetSpeedJson")
        streetSpeedJson.init()
        for time in timeRoadSpeed:
            streetSpeedJson.data = timeRoadSpeed[time]
            putout({"streetSpeedJson": {time - timenow: streetSpeedJson}})


def newSpeed(v0: float, depth: float):
    x = depth / 10  # mm -> cm
    a = 7.5
    b = 3
    v0 = v0 * 0.1
    v = 0.5 * v0 * math.tanh((-x + a) / b) + 0.5 * v0
    return v, (v - v0) / v0


def listMean(list: Sequence):
    if len(list) == 0:
        return 0
    return sum(list) / len(list)
