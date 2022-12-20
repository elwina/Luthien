from typing import TypedDict
from core.tools.raster2Txt import raster2Txt
from core.typing.recordType import TYPE_Recorder_Data, TYPE_Recorder_Env
from core.recorderGlobal import recorderGlobal as rGl


def rasterRecorder(rec: TYPE_Recorder_Data) -> None:
    rdata = rec['data']
    tempEnv = rec['tempEnv']
    recEnv: TYPE_Recorder_Env = {
        "insName": tempEnv['insName'],
        "fileType": ".ascii",
        "ifModule": tempEnv["ifModule"],
        "linkDes": tempEnv["linkDes"],
        "recNum": 0
    }
    filename = rGl.geneFilename(recEnv)
    raster2Txt(rdata, filename)
