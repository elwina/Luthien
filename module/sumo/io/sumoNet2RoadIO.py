import os
from pathlib import Path
import shutil
from typing import MutableMapping, cast
from copy import deepcopy

from core.typing.ioType import TYPE_IO_Data

"""
config:
    filepath: str

    outEdge: bool

    outProj:int
    inProj:int

"""


def sumoNet2RoadIO(ioData: TYPE_IO_Data) -> int:
    from core.field.roadField import RoadField

    ins: RoadField = cast(RoadField, ioData["ins"])
    config = ioData["config"]

    filepath = config["filepath"]
    if "outEdge" in config and config["outEdge"] == True:
        from module.sumo.tools.extractStreet import extractEdge2MultiLineString

        newins = extractEdge2MultiLineString(filepath)
    else:
        from module.sumo.tools.extractStreet import extractStreet2MultiLineString

        newins = extractStreet2MultiLineString(filepath)

    if "outProj" in config and "inProj" in config:
        newins.trans2Proj(config["inProj"], config["outProj"])

    ins.data = deepcopy(newins.data)
    return 0
