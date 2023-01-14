import os
from pathlib import Path
import shutil
from typing import MutableMapping
from core.typing.ioType import TYPE_IO_DATA


def fileListIO(ioData: TYPE_IO_DATA) -> TYPE_IO_DATA:
    config = ioData["config"]
    fname=config["fname"]
    oldData: MutableMapping[str, str] = ioData["oldData"]
    newData:MutableMapping[str,str] = ioData["newData"]

    for i,v in newData.items():
        newpath=os.path.join("temp",fname,Path(v).name)
        shutil.copyfile(v,newpath)
        newData[i]=newpath

    finalData={}
    finalData.update(oldData)
    finalData.update(newData)

    ioData["newData"] = finalData
    return ioData
