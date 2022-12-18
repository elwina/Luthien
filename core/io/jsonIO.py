import commentjson as json
from core.typing.ioType import TYPE_IO_DATA
from typing import TypedDict
from loguru import logger
'''
config
    outListConf:True  # 以listConf中的out输出

    inFile:True # 以文件的形式输入配置
    inFilePath:"" # 文件路径
'''


def jsonIO(ioData: TYPE_IO_DATA) -> TYPE_IO_DATA:
    config = ioData["config"]
    oldData = ioData["oldData"]
    data = {}
    if "inFile" in config and config["inFile"] == True:
        data = _inFromFile(config["inFilePath"])

    if "outListConf" in config and config["outListConf"] == True:
        for name in data:
            oldData[name] = data[name]
        ioData["newData"] = oldData
    return ioData


def _inFromFile(filepath) -> dict:
    logger.info("Read Json File {path}", path=filepath)
    with open(filepath) as fp:
        re = json.load(fp)
        return re