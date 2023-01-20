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
