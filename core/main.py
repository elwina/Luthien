import getopt
import sys
from loguru import logger
from core.control import Controller

# 初始化一些Global单例类
from config.register import IO_LIST, RECORDER_LIST, MODULE_LIST, BASE_LIST, FIELD_LIST
from core.recorderGlobal import recorderGlobal
from core.configGlobal import configGlobal


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
    logger.add(configGlobal.getConfig()["basic"]["outputPath"] + "main.log",
               mode="w")
    logger.info("Log system starts running.")

    # 初始化结束

    # 开始运行
    logger.info("Controller starts running.")
    ct = Controller()
    ct.run()
