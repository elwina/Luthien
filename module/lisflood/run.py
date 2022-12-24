import math
import os
import shutil
import subprocess
from typing import Any, Callable, MutableMapping, Sequence, cast

from loguru import logger
from core.base.rasterType import TYPE_RASTER_DATA
from core.io.txt2RasterIO import txt2RasterIO
from core.tools.dict2Txt import dict2Txt
from core.tools.raster2Txt import raster2Txt
from core.typing.fieldType import TYPE_Instance
from core.typing.outputType import TYPE_Putout

from copy import deepcopy

MODULE_ROOT = "module/lisflood/"


def sampleRun(putout: Callable[[TYPE_Putout], None],
              instances: MutableMapping[str, TYPE_Instance],
              optList: Sequence[str]):
    logger.debug("Module Lisflood Run,optList:{opt}", opt=",".join(optList))

    ifManni = False
    if "mann" in optList: ifManni = True

    # 新建temp文件夹
    tempDir = os.path.join(MODULE_ROOT, "temp")
    shutil.rmtree(tempDir)
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
        strList.append("0\t" + str(rainBase) + "\n")
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

    subprocess.run(["../bin/lisflood", "auto.par"], cwd=tempDir)

    water1h = os.path.join(tempDir, "results", "res-0001.wd")
    from core.field.rainField import RainField
    water = RainField()
    water.init()
    water.define(txt2RasterIO, {"inFile": True, "inFilePath": water1h}, None)
    putout({"water": {0: water}})
