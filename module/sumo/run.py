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

    cmd.append("--end")
    cmd.append("43200")

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

    outputFiles = {}
    if config.getOne("out--tripinfo-output") == 1:
        tripinfoFilename = os.path.join("res", "res.tripinfo.xml")
        cmd.append("--tripinfo-output")
        cmd.append(tripinfoFilename)
        tripinfoFilename = os.path.join(tempDir, tripinfoFilename)
        outputFiles["tripinfo"] = tripinfoFilename
    if config.getOne("out--summary") == 1:
        summaryFilename = os.path.join("res", "res.summary.xml")
        cmd.append("--summary")
        cmd.append(summaryFilename)
        summaryFilename = os.path.join(tempDir, summaryFilename)
        outputFiles["summary"] = summaryFilename
    if config.getOne("out--lanedata-output") == 1:
        lanedataFilename = os.path.join("res", "res.lanedata.xml")
        cmd.append("--lanedata-output")
        cmd.append(lanedataFilename)
        lanedataFilename = os.path.join(tempDir, lanedataFilename)
        outputFiles["lanedata"] = lanedataFilename
    if config.getOne("out--queue-output") == 1:
        queueFilename = os.path.join("res", "res.queue.xml")
        cmd.append("--queue-output")
        cmd.append(queueFilename)
        queueFilename = os.path.join(tempDir, queueFilename)
        outputFiles["queue"] = queueFilename

    subprocess.run(cmd, shell=True, cwd=tempDir)

    if outputFiles != {}:
        Files = TempFileField()
        Files.init()
        Files.define(fileListIO, {}, outputFiles)
        putout({"files": {0: Files}})
