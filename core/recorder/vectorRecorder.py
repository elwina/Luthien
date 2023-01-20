from pathlib import Path
import shutil
from typing import MutableMapping
from core.typing.recordType import TYPE_Recorder_Data, TYPE_Recorder_Env

from core.recorderGlobal import recorderGlobal as rGl
'''
config:
"geojson": true 
'''


def vectorRecorder(rec: TYPE_Recorder_Data) -> None:
    from core.base.vector import VectorBase
    ins: VectorBase = rec['ins']
    tempEnv = rec['tempEnv']
    recEnv: TYPE_Recorder_Env = {
        "insName": tempEnv['insName'],
        "fileType": ".geojson",
        "ifModule": tempEnv["ifModule"],
        "linkDes": tempEnv["linkDes"],
        "recNum": 0
    }
    filename = rGl.geneFilename(recEnv)
    f = open(filename, "w", encoding="utf-8")
    f.write(ins.toGeoJSONString())
    f.close()
