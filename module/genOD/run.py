import json
import os
import shutil

from typing import Any, Callable, MutableMapping, Sequence, cast

import pandas as pd
from core.typing.fieldType import TYPE_Instance
from core.typing.outputType import TYPE_Putout

from module.genOD.information import MODULE_ROOT

from loguru import logger


def genODRun(
    putout: Callable[[TYPE_Putout], None],
    instances: MutableMapping[str, TYPE_Instance],
    optList: Sequence[str],
):
    logger.debug("Module genOD Run,optList:{opt}.", opt=",".join(optList))

    # 新建temp文件夹
    tempDir = os.path.join(MODULE_ROOT, "temp")
    shutil.rmtree(tempDir, ignore_errors=True)
    os.mkdir(tempDir)

    from core.base.listConf import ListConfBase

    uni = cast(ListConfBase, instances["genODUni"])

    from core.field.tempFileField import TempFileField

    files = cast(TempFileField, instances["files"])

    with open(files.getAFilePath("action"), "r", encoding="utf-8") as f:
        action = json.load(f)
    with open(files.getAFilePath("config"), "r", encoding="utf-8") as f:
        config = json.load(f)

    # 生成trips
    from module.genOD.tools.actionGen import actionGen

    trip, trace = actionGen(action, config)

    if uni.getOne("allocate") == 1:
        # 随机分配
        with open(files.getAFilePath("place"), "r", encoding="utf-8") as f:
            placeConf = json.load(f)

        buildingID = cast(str, uni.getOne("buildingID"))

        from core.field.buildingField import BuildingField

        building = cast(BuildingField, instances["building"])

        places = {}

        for place in placeConf:
            string = placeConf[place]
            if string[0] != "!":
                targets = building.getAllObjByOneProp(string, 1)
            else:
                targets = building.getAllObjByOneProp(string[1:], 0)

            works = list(map(lambda x: x.properties[buildingID], targets))
            places[place] = works

        from module.genOD.tools.allocateWork import allocateWork

        newTrip = allocateWork(trip, config, places)
        trip = newTrip

    from core.base.json import JsonBase

    ODJson = JsonBase("ODJson")
    ODJson.init()
    ODJson.setJsonData(trip)
    putout({"ODJson": {0: ODJson}})
    TraceJson = JsonBase("TraceJson")
    TraceJson.init()
    TraceJson.setJsonData(trace)
    putout({"TraceJson": {0: TraceJson}})

    # 生成OD表
    from core.base.table import TableBase

    ODTable = TableBase()
    ODTable.init()

    ODTable.setPandasData(pd.DataFrame(trip))
    putout({"ODTable": {0: ODTable}})
