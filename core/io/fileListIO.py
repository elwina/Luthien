import os
from pathlib import Path
import shutil
from typing import MutableMapping, cast
from core.typing.ioType import TYPE_IO_Data


def fileListIO(ioData: TYPE_IO_Data) -> TYPE_IO_Data:
    from core.base.file import FileBase

    config = ioData["config"]
    fname = config["fname"]
    
    ins = cast(FileBase, ioData["ins"])
    oldData: MutableMapping[str, str] = (cast(FileBase, ioData["ins"])).data
    newData: MutableMapping[str, str] = ioData["newData"]

    for i, v in newData.items():
        newpath = os.path.join("temp", fname, Path(v).name)
        shutil.copyfile(v, newpath)
        newData[i] = newpath

    finalData = {}
    finalData.update(oldData)
    finalData.update(newData)

    ioData["newData"]=finalData
    ins.data = finalData
    return ioData
