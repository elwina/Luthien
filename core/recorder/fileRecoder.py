from pathlib import Path
import shutil
from typing import MutableMapping
from core.typing.recordType import TYPE_Recorder_Data, TYPE_Recorder_Env

from core.recorderGlobal import recorderGlobal as rGl
'''
config:
all true 记录所有文件
filelist []记录什么文件
'''


def fileRecorder(rec: TYPE_Recorder_Data) -> None:
    fdata: MutableMapping[str, str] = rec['ins'].data
    config: MutableMapping[str, str] = rec["config"]

    files = []
    if "all" in config and config['all'] == True:
        files = fdata.values()
    elif "filelist" in config.keys():
        files = config["filelist"]

    for i, f in enumerate(files):
        tempEnv = rec['tempEnv']
        recEnv: TYPE_Recorder_Env = {
            "insName": tempEnv['insName'],
            "fileType": "".join(Path(f).suffixes),
            "ifModule": tempEnv["ifModule"],
            "linkDes": tempEnv["linkDes"],
            "recNum": i
        }
        filename = rGl.geneFilename(recEnv)
        shutil.copyfile(f, filename)
