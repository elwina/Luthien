from math import log10
import os
import shutil

from typing import Any, Callable, MutableMapping, Sequence, cast
from core.field.tempFileField import TempFileField
from core.typing.fieldType import TYPE_Instance
from core.typing.outputType import TYPE_Putout

from module.geneRain.information import MODULE_ROOT

from loguru import logger


def geneRainRun(
    putout: Callable[[TYPE_Putout], None],
    instances: MutableMapping[str, TYPE_Instance],
    optList: Sequence[str],
):
    logger.debug("Module geneRain Run,optList:{opt}.", opt=",".join(optList))

    # 新建temp文件夹
    tempDir = os.path.join(MODULE_ROOT, "temp")
    shutil.rmtree(tempDir, ignore_errors=True)
    os.mkdir(tempDir)

    from core.base.listConf import ListConfBase

    uni = cast(ListConfBase, instances["geneRainUni"])

    # 芝加哥雨型
    A1, A2, P, B, C, r = uni.getManyFloats(["A1", "A2", "P", "B", "C", "r"])
    totalMinutes = cast(int, uni.getOne("totalMinutes"))
    date = uni.getOne("date")
    rainGage = uni.getOne("rainGage")

    rains = []
    A = A1 * (1 + A2 * log10(P))
    for t in range(totalMinutes):
        if t <= float(r) * totalMinutes:
            t = totalMinutes / 2 - t
            val = 60 * A * ((1 - C) * t / r + B) / ((t / r + B) ** (C + 1))
            rains.append(val)
        else:
            t = t - totalMinutes / 2
            val = 60 * A * ((1 - C) * t / (1 - r) + B) / ((t / (1 - r) + B) ** (C + 1))
            rains.append(val)

    rainFile = TempFileField()
    rainPath = os.path.join(tempDir, "autorain.txt")
    with open(rainPath, "w", encoding="utf-8") as fp:
        for t in range(totalMinutes):
            h = "%02d" % (int(t) // 60)
            m = "%02d" % (int(t) % 60)
            cin = f"{rainGage} {date} {h} {m} {rains[t]}\n"
            fp.write(cin)

    from core.io.fileListIO import fileListIO

    rainFile.define(fileListIO, {}, {"rain": rainPath})
    putout({"rainFile": {0: rainFile}})
