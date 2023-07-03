import math
import subprocess
import os
import platform
import shutil
from pyswmm import Output
from swmm.toolkit.shared_enum import NodeAttribute

from typing import Any, Callable, MutableMapping, Sequence, cast
from core.base.file import FileBase
from core.base.json import JsonBase
from core.typing.fieldType import TYPE_Instance
from core.typing.outputType import TYPE_Putout

from module.swmm.information import MODULE_ROOT

from loguru import logger

from module.swmm.tools.nodeExtract import nodeExtract


def swmmRun(putout: Callable[[TYPE_Putout], None],
            instances: MutableMapping[str,
                                      TYPE_Instance], optList: Sequence[str]):
    logger.debug("Module swmm Run,optList:{opt}.", opt=",".join(optList))

    # 新建temp文件夹
    tempDir = os.path.join(MODULE_ROOT, "temp")
    shutil.rmtree(tempDir, ignore_errors=True)
    os.mkdir(tempDir)

    from core.base.listConf import ListConfBase
    uni = cast(ListConfBase, instances["swmmUni"])

    rainGage = cast(str, uni.getOne("rainFileName"))

    rainFile = cast(FileBase, instances["rainFile"])
    rainPath = os.path.join(tempDir, rainGage)
    rainFile.getFile("rain", rainPath)

    inpFile = cast(FileBase, instances["inpFile"])
    inpPath = os.path.join(tempDir, "auto.inp")
    inpFile.getFile("inp", inpPath)

    rptPath = os.path.join(tempDir, "rpt.txt")
    outPath = os.path.join(tempDir, "auto.out")
    cmd = ["swmm", "auto.inp", "rpt.txt", "auto.out"]

    system = platform.system()
    if system == "Windows":
        cmd[0] = os.path.join("..\\bin\\runswmm.exe")
        subprocess.run(cmd, shell=True, cwd=tempDir)

    nodeIns = nodeExtract(inpPath)
    # nodeIns.trans2Proj(3395, 32650)

    pjson: dict[str, list[float]] = {}

    totalTime = cast(int, uni.getOne("totalTime"))
    with Output(outPath) as out:
        floodData: dict[str, float] = out.node_attribute(
            NodeAttribute.FLOODING_LOSSES,  # type: ignore
            0)  # type: ignore
        for key in floodData:
            pjson[key] = []

        for t in range(totalTime):
            floodData: dict[str, float] = out.node_attribute(
                NodeAttribute.FLOODING_LOSSES,  # type: ignore
                t)  # type: ignore
            pondData: dict[str, float] = out.node_attribute(
                NodeAttribute.TOTAL_INFLOW,  # type: ignore
                t)  # type: ignore
            # print(floodData)

            for obj in nodeIns.data.objects:
                nodeid = obj.properties["nodeid"]
                if nodeid in floodData:
                    # obj.properties["flood"] = floodData[nodeid]
                    if math.isclose(floodData[nodeid], 0.0):
                        #pjson[nodeid].append(-pondData[nodeid])
                        pjson[nodeid].append(0.0)
                    else:
                        pjson[nodeid].append(floodData[nodeid])
            # putout({"floodNode": {t: nodeIns}})

    for h in range(totalTime // 60):
        for obj in nodeIns.data.objects:
            nodeid = obj.properties["nodeid"]
            if nodeid in pjson:
                obj.properties["flood"] = getHourSum(pjson[nodeid], h)
        putout({"floodNode": {h: nodeIns}})

    # pointWaterJson
    pointWaterJson = JsonBase("pointWater")
    pointWaterJson.init()
    pointWaterJson.data = pjson
    putout({"pointWaterJson": {0: pointWaterJson}})


def getHourSum(list: list[float], hour):
    re: float = 0
    for i in range(hour * 60, (hour + 1) * 60):
        if i > list.__len__():
            continue
        else:
            re = re + list[i]
    return re