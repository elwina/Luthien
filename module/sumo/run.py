import math
import os
from pathlib import Path
import shutil
import subprocess
import platform
from uuid import uuid4

from typing import Any, Callable, MutableMapping, Sequence, cast
from core.field.tempFileField import TempFileField
from core.io.fileListIO import fileListIO
from core.typing.fieldType import TYPE_Instance
from core.typing.outputType import TYPE_Putout

from module.sumo.information import MODULE_ROOT

from core.io.rasterIO import rasterIO
from core.tools.dict2Txt import dict2Txt
from core.tools.raster2Txt import raster2Txt

from loguru import logger


def sumoRun(putout: Callable[[TYPE_Putout], None],
            instances: MutableMapping[str,
                                      TYPE_Instance], optList: Sequence[str]):
    logger.debug("Module sumo Run,optList:{opt}.", opt=",".join(optList))

    # 新建temp文件夹
    tempDir = os.path.join(MODULE_ROOT, "temp")
    shutil.rmtree(tempDir, ignore_errors=True)
    os.mkdir(tempDir)

    from core.base.listConf import ListConfBase
    config = cast(ListConfBase, instances["sumoUni"])

    networkFilename = os.path.join(tempDir, "auto.net.xml")
    networkIns = instances["network"]
    networkIns = cast(TempFileField, networkIns)
    networkIns.getFile("sumoNet", networkFilename)

    cmd: Sequence[str] = ["sumo"]
    cmd.append("--net-file")
    cmd.append("auto.net.xml")

    if "routeFiles" in instances and config.getOne("routeFiles") == 1:
        routeFilename = os.path.join(tempDir, "auto.route.xml")
        routeFilesIns = cast(TempFileField, instances["routeFiles"])
        routeFilesIns.getFile("route", routeFilename)

        cmd.append("--route-files")
        cmd.append("auto.route.xml")

    if "addFiles" in instances and config.getOne("addFiles") == 1:
        addFilesIns = cast(TempFileField, instances["addFiles"])
        allAddFiles = addFilesIns.getFileNames()
        filePaths = []
        for addFile in allAddFiles:
            filePath = str(uuid4()) + ".add.xml"
            addFilesIns.getFile(addFile, os.path.join(tempDir, filePath))
            filePaths.append(filePath)
        cmd.append("--additional-files")
        cmd.append(",".join(filePaths))

    resDir = os.path.join(tempDir, "res")
    os.mkdir(resDir)

    outputFiles = []
    if config.getOne("out--tripinfo-output") == 1:
        global tripinfoFilename
        tripinfoFilename = os.path.join("res", "res.tripinfo.xml")
        cmd.append("--tripinfo-output")
        cmd.append(tripinfoFilename)
        tripinfoFilename = os.path.join(tempDir, tripinfoFilename)
        outputFiles.append(tripinfoFilename)

    subprocess.run(cmd, shell=True, cwd=tempDir)

    Files = TempFileField()
    Files.init()
    Files.define(fileListIO, {}, {
        "tripinfo": tripinfoFilename,
    })
    putout({"files": {0: Files}})
    if config.getOne("out--tripinfo-output") == 1:
        putout({"files": {0: Files}})