import commentjson as json
from pathlib import Path
import shutil
from typing import MutableMapping
from core.typing.recordType import TYPE_Recorder_Data, TYPE_Recorder_Env

from core.recorderGlobal import recorderGlobal as rGl
'''
config:
'''


def jsonRecorder(rec: TYPE_Recorder_Data) -> None:
    data: MutableMapping[str, str] = rec['ins'].data
    config: MutableMapping[str, str] = rec["config"]

    tempEnv = rec['tempEnv']
    recEnv: TYPE_Recorder_Env = {
        "insName": tempEnv['insName'],
        "fileType": ".json",
        "ifModule": tempEnv["ifModule"],
        "linkDes": tempEnv["linkDes"],
        "recNum": 0
    }
    filename = rGl.geneFilename(recEnv)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
