import getopt
import os
import shutil
import sys

from core.controller import Controller

# 初始化一些Global单例类
from config.register import IO_LIST, RECORDER_LIST, MODULE_LIST, BASE_LIST, FIELD_LIST
from core.recorderGlobal import recorderGlobal
from core.configGlobal import configGlobal
from core.envGlobal import envGlobal
from loguru import logger


def start():
    try:
        opts, args = getopt.getopt(sys.argv[2:], "c:", [])
        for opt, arg in opts:
            if "-c" == opt:
                configGlobal.setConfig(arg)

    except getopt.GetoptError:
        print("Wrong Command Line!")
        print("Exit!")
        sys.exit(2)

    # 初始化步骤开始
    # 初始化配置
    configGlobal.initConfig()

    # 初始化日志记录
    logger.add(
        configGlobal.getConfig()["basic"]["outputPath"] + "main.log",
        mode="w",
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "{extra[type]} | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    mainLogger = logger.bind(type="main")
    mainLogger.info("Log system starts running.")

    # 新建temp目录
    tempDir = os.path.join("temp/")
    shutil.rmtree(tempDir, ignore_errors=True)
    os.mkdir(tempDir)

    # 初始化结束

    # 开始运行
    mainLogger.info("Controller starts running.")
    ct = Controller()
    envGlobal.ct = ct
    ct.run()

    # 运行结束
    mainLogger.info("Controller ends running.")
