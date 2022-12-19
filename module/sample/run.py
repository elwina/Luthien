from typing import Callable, MutableMapping, Sequence

from loguru import logger
from core.tools.raster2Txt import raster2Txt
from core.typing.fieldType import TYPE_Instance
from core.typing.outputType import TYPE_Putout

from copy import deepcopy


def sampleRun(putout: Callable[[TYPE_Putout], None],
              instances: MutableMapping[str, TYPE_Instance],
              optList: Sequence[str], env):
    logger.debug("sampleRun,optList:{opt}", opt=",".join(optList))

    dem = deepcopy(instances["dem"])
    dem.data["row"] = dem.data["row"] + 1

    print(dem.data["row"])

    putout({"rain": {0: dem}})

    #raster2Txt(rasterData, "output/test.dem.ascii")
