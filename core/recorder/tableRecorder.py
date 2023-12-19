from pathlib import Path
import shutil
from typing import MutableMapping, cast
from core.typing.recordType import TYPE_Recorder_Data, TYPE_Recorder_Env

from core.recorderGlobal import recorderGlobal as rGl

"""
config:
type: csv
"""


def tableRecorder(rec: TYPE_Recorder_Data) -> None:
    config: MutableMapping[str, str] = rec["config"]

    if "type" in config and config["type"] == "csv":
        tempEnv = rec["tempEnv"]
        recEnv: TYPE_Recorder_Env = {
            "insName": tempEnv["insName"],
            "fileType": ".csv",
            "ifModule": tempEnv["ifModule"],
            "linkDes": tempEnv["linkDes"],
            "recNum": 0,
        }
        filename = rGl.geneFilename(recEnv)

        from core.base.table import TableBase

        ins = cast(TableBase, rec["ins"])
        ins.toCSVFile(filename)
