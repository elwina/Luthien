from copy import deepcopy

from typing import Any, Callable, MutableMapping, Sequence, cast
from core.base.listConf import ListConfBase
from core.base.raster import RasterBase
from core.typing.fieldType import TYPE_Instance
from core.typing.outputType import TYPE_Putout

from loguru import logger


def landslideEvaRun(putout: Callable[[TYPE_Putout], None],
                    instances: MutableMapping[str, TYPE_Instance],
                    optList: Sequence[str]):
    logger.debug("Module landslide Run,optList:{opt}.", opt=",".join(optList))

    threshold = 0.2
    if "lanUni" in optList:
        lanUni = cast(ListConfBase, instances["lanUni"])
        threshold = cast(float, lanUni.getOne("threshold"))

    waterIns = cast(RasterBase, instances["water"])
    evaIns = deepcopy(waterIns)
    evaIns.data.radata = _judge(evaIns.data.radata, threshold)

    putout({"eva": {0: evaIns}})


def _judge(radata: Sequence[Sequence[float]],
           threshold: float) -> Sequence[Sequence[int]]:
    return list(
        map(lambda row: list(map(lambda x: 1
                                 if x >= threshold else 0, row)), radata))
