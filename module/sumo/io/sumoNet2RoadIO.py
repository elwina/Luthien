import os
from pathlib import Path
import shutil
from typing import MutableMapping, cast
from copy import deepcopy

from core.typing.ioType import TYPE_IO_Data
'''
config:
    filepath: str

    outEdge: bool
'''


def sumoNet2RoadIO(ioData: TYPE_IO_Data) -> TYPE_IO_Data:
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

    ins.data = deepcopy(newins.data)
    ioData["newData"] = deepcopy(ins.data)
    return ioData
