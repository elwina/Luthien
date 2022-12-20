from loguru import logger
from core.conf import getConfig
from core.control import Control
from core.recorderGlobal import recorderGlobal


def start():
    logger.add(getConfig()["basic"]["outputPath"] + "main.log", mode="w")

    ct = Control()
    ct.run()
