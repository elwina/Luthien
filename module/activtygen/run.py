import os
import shutil

from typing import Any, Callable, MutableMapping, Sequence,cast
from core.typing.fieldType import TYPE_Instance
from core.typing.outputType import TYPE_Putout

from module.activtygen.information import MODULE_ROOT

from loguru import logger


def activtygenRun(putout: Callable[[TYPE_Putout], None],
                    instances: MutableMapping[str, TYPE_Instance],
                    optList: Sequence[str]):
    logger.debug("Module activtygen Run,optList:{opt}.", opt=",".join(optList))

    # 新建temp文件夹
    tempDir = os.path.join(MODULE_ROOT, "temp")
    shutil.rmtree(tempDir, ignore_errors=True)
    os.mkdir(tempDir)

    from core.base.listConf import ListConfBase
    uni = cast(ListConfBase, instances["activtygenUni"])