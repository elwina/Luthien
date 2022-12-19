from typing import MutableMapping, Sequence

from loguru import logger
from core.tools.raster2Txt import raster2Txt
from core.typing.fieldType import TYPE_Instance


def sampleRun(instances: MutableMapping[str, TYPE_Instance],
              optList: Sequence[str]):
    logger.debug("sampleRun,optList:{opt}", opt=",".join(optList))

    dem = instances["dem"]
    row = dem.data["row"]
    dem.data["row"] = dem.data["row"] + 1
    print(row)
    #raster2Txt(rasterData, "output/test.dem.ascii")
