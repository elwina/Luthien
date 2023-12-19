from typing import Any
import commentjson as json

from core.typing.ioType import TYPE_IO_Data

from loguru import logger

"""
config
    outListConf:True  #* 以listConf中的out输出
    outJson:True #* 以jsonBase的形式输出

    inFile:True #* 以文件的形式输入配置
    inFilePath:"" #* 文件路径
"""


def jsonIO(ioData: TYPE_IO_Data) -> int:
    from core.base.listConf import ListConfBase

    config = ioData["config"]
    ins: ListConfBase = ioData["ins"]
    oldData = ioData["ins"].data
    data = {}
    if "inFile" in config and config["inFile"] == True:
        data = _inFromFile(config["inFilePath"])

    if "outListConf" in config and config["outListConf"] == True:
        for name in data:
            oldData[name] = data[name]
        data = oldData

    ins.data = data

    return 0


def _inFromFile(filepath) -> Any:
    logger.info("Read json file {path}", path=filepath)
    try:
        with open(filepath, encoding="utf-8") as fp:
            re = json.load(fp)
            return re
    except Exception as e:
        logger.error(e)
        logger.error("Cannot read the file {path}!", path=filepath)
        return -1
