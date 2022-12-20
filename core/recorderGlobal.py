from loguru import logger
from core.env import env
from core.conf import getConfig
from core.typing.recordType import TYPE_Recorder_Env


class RecorderGlobal:
    fileList: list[str] = []

    def geneFilename(self, recEnv: TYPE_Recorder_Env) -> str:
        strList: list[str] = []

        module = env.moduleNow if recEnv["ifModule"] else "main"
        strList.append(module)
        strList.append(recEnv["insName"])
        strList.append(str(env.epoch))

        linkDes = recEnv["linkDes"]
        strList.append(linkDes)

        strList.append(str(recEnv["recNum"]))

        path = getConfig()["basic"]["outputPath"]
        filename = path + "_".join(strList) + recEnv["fileType"]
        self._takeRecord(filename)
        logger.info("Generate filename {name}", name=filename)
        return filename

    def _takeRecord(self, filename: str):
        self.fileList.append(filename)


recorderGlobal = RecorderGlobal()
