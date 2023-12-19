import os
from pathlib import Path
import shutil
from uuid import uuid4

from typing import Mapping, MutableMapping, Tuple, cast
from core.typing.ioType import TYPE_IO_Data

"""
多个file ins合并为一个
config:
inAll 全部合并,不规避冲突
inFileIns: ["ins1","ins2"]
inDetail: {
    name: "instance:inname"
}

data中存放新加的文件
"""


def fileMergeIO(ioData: TYPE_IO_Data) -> int:
    from core.base.file import FileBase

    config = ioData["config"]
    fname = config["fname"]

    ins = cast(FileBase, ioData["ins"])
    oldData: MutableMapping[str, str] = (cast(FileBase, ioData["ins"])).data
    newData: MutableMapping[str, str] = ioData["newData"]

    for i, v in newData.items():
        newpath = os.path.join("temp", fname, str(uuid4()) + "".join(Path(v).suffixes))
        shutil.copyfile(v, newpath)
        newData[i] = newpath

    finalData = {}
    finalData.update(oldData)
    finalData.update(newData)

    from core.envGlobal import envGlobal as eGl
    from core.instanceManager import InstanceManager as IMR

    EGL_iMr: IMR = eGl.ct.iMr
    if config.get("inAll", False) == True:
        for inInsName in config.get("inFileIns", []):
            inIns = EGL_iMr.getInstance(inInsName)
            inIns = cast(FileBase, inIns)
            for name in inIns.getFileNames():
                oldPath = inIns.getAFilePath(name)
                newpath = os.path.join(
                    "temp", fname, str(uuid4()) + "".join(Path(oldPath).suffixes)
                )
                inIns.getFile(name, newpath)
                finalData.update({name: newpath})
    elif config.get("inDetail", None) is not None:
        detail: Mapping[str, str] = config["inDetail"]
        for name, deStr in detail.items():
            insName, fileName = _parseFile(deStr)
            if insName != "":
                inIns = EGL_iMr.getInstance(insName)
                inIns = cast(FileBase, inIns)
                oldPath = inIns.getAFilePath(fileName)
                newpath = os.path.join(
                    "temp", fname, str(uuid4()) + "".join(Path(oldPath).suffixes)
                )
                inIns.getFile(fileName, newpath)
                finalData.update({name: newpath})

    ins.data = finalData
    return 0


def _parseFile(str: str) -> Tuple[str, str]:
    arr = str.split(":")
    if arr.__len__() < 2:
        return ("", "")

    return (arr[0], arr[1])
