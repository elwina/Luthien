import math
import os
from pathlib import Path
import shutil
import subprocess
import platform

from typing import Any, Callable, MutableMapping, Sequence, cast
from core.io.fileListIO import fileListIO
from core.typing.fieldType import TYPE_Instance
from core.typing.outputType import TYPE_Putout

from module.lisflood.information import MODULE_ROOT

from core.io.rasterIO import rasterIO
from core.tools.dict2Txt import dict2Txt
from core.tools.raster2Txt import raster2Txt

from loguru import logger


def lisfloodRun(putout: Callable[[TYPE_Putout], None],
                instances: MutableMapping[str, TYPE_Instance],
                optList: Sequence[str]):
    logger.debug("Module Lisflood Run,optList:{opt}.", opt=",".join(optList))

    ifManni = False
    if "mann" in optList: ifManni = True

    # 新建temp文件夹
    tempDir = os.path.join(Path(MODULE_ROOT), "temp")
    shutil.rmtree(tempDir, ignore_errors=True)
    os.mkdir(tempDir)

    from core.base.listConf import ListConfBase
    config = cast(ListConfBase, instances["lisUni"])
    if config.getOne("rainFromConf") == 1:
        # 生成.rain
        rainBase = cast(int, config.getOne("rainBase"))
        rainAddPerhour = cast(int, config.getOne("rainAddPerhour"))
        simTime = cast(int, config.getOne("simTime"))
        totalHours = math.ceil(simTime / 60 / 60)

        strList = [
            "# Auto Generated\n",
            str(totalHours + 1) + "\t"
            "hours"
            "\n"
        ]
        strList.append(str(rainBase) + "\t0" + "\n")
        for hourM1 in range(totalHours):
            hour = hourM1 + 1
            rainIn = rainBase + hour * rainAddPerhour
            strList.append(str(rainIn) + "\t" + str(hour) + "\n")
        rainString = "".join(strList)
        rainFilename = os.path.join(tempDir, "auto.rain")
        with open(rainFilename, "w") as fp:
            fp.write(rainString)
    else:
        rainFilename = ""

    from core.field.demField import DemField
    dem = cast(DemField, instances["dem"])
    demFilename = os.path.join(tempDir, "dem.ascii")
    raster2Txt(dem.data, demFilename)

    parDict = {
        "DEMfile": "dem.ascii",
        "resroot": "res",
        "dirroot": "results",
        "sim_time": config.getOne("simTime"),
        "initial_tstep": 1.0,
        "massint": 100,
        "saveint": config.getOne("saveInt"),
        "fpfric": config.getOne("fpfric"),
        "rainfall": "auto.rain",
        "adaptoff": ""
    }
    parFilename = os.path.join(tempDir, "auto.par")
    dict2Txt(parDict, parFilename)

    system = platform.system()
    if system == "Windows":
        subprocess.run(["..\\bin\\lisflood.exe", "auto.par"],
                       shell=True,
                       cwd=tempDir)

    elif system == "Linux":
        subprocess.run(["../bin/lisflood", "auto.par"], cwd=tempDir)

    from core.field.waterField import WaterField
    recordNum = cast(int, config.getOne("recordNum"))
    for i in range(recordNum):
        nameNum = "%04d" % i
        outWaterFileName = os.path.join(tempDir, "results",
                                        "res-%s.wd" % nameNum)
        water = WaterField()
        water.init()
        water.define(rasterIO, {
            "inDriver": "AAIGrid",
            "inFilePath": outWaterFileName
        }, None)
        # 从meter转换为mm
        water.timesANum(1000)
        water.data.xllCorner, water.data.yllCorner, water.data.cellSize = dem.data.xllCorner, dem.data.yllCorner, dem.data.cellSize
        putout({"water": {i: water}})
        pass

    from core.field.tempFileField import TempFileField
    Files = TempFileField()
    Files.init()
    Files.define(fileListIO, {}, {
        "mass": os.path.join(tempDir, "results", "res.mass"),
        "max": os.path.join(tempDir, "results", "res.max"),
    })
    putout({"files": {0: Files}})
