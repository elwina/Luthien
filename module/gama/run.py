import os
import shutil
import subprocess
from pathlib import PurePath

from typing import Any, Callable, MutableMapping, Sequence, cast
from core.typing.fieldType import TYPE_Instance
from core.typing.outputType import TYPE_Putout

from module.gama.information import MODULE_ROOT

from loguru import logger


def gamaRun(
    putout: Callable[[TYPE_Putout], None],
    instances: MutableMapping[str, TYPE_Instance],
    optList: Sequence[str],
):
    # logger.debug("Module gama Run,optList:{opt}.", opt=",".join(optList))

    # 新建temp文件夹
    tempDir = os.path.join(MODULE_ROOT, "temp")
    shutil.rmtree(tempDir, ignore_errors=True)
    os.mkdir(tempDir)

    from core.base.listConf import ListConfBase

    # uni = cast(ListConfBase, instances["gamaUni"])

    # 生成gama配置文件
    from module.gama.tool.gamaConfig import gamaConfig

    target = os.path.join(tempDir, "model.gaml")
    gamaConfig(
        target,
        {
            "total_people": 100,
            "building_shapefile": os.path.abspath(
                "module/gama/includes/buildings_block_utf8.shp"
            ),
            "road_shapefile": os.path.abspath("module/gama/includes/road.shp"),
            "trip_csv_file": os.path.abspath("module/gama/includes/trip.csv"),
            "buildingID": "BID",
            "saveCarsOnRoadFolder": os.path.abspath(tempDir),
        },
    )

    print(PurePath(os.path.abspath("module/gama/includes/road.shp")).as_posix())

    pathabs = os.path.abspath(target)
    subprocess.run(
        "gama-headless.bat -batch road_traffic " + pathabs,
        shell=True,
        cwd="C:\\Program Files\\Gama\\headless",
    )


gamaRun(0, 0, 0)
