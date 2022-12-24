from loguru import logger
from core.envGlobal import envGlobal
from core.configGlobal import configGlobal
from core.typing.recordType import TYPE_Recorder_Env


class RecorderGlobal:
    fileList: list[str] = []
    total = 0

    def geneFilename(self, recEnv: TYPE_Recorder_Env) -> str:
        strList: list[str] = []

        strList.append("Out")
        strList.append(str(self.total))
        self.total = self.total + 1

        module = envGlobal.moduleNow if recEnv["ifModule"] else "main"
        strList.append(module)
        strList.append(recEnv["insName"])
        strList.append(str(envGlobal.epoch))

        linkDes = recEnv["linkDes"]
        strList.append(linkDes)

        strList.append(str(recEnv["recNum"]))

        path = configGlobal.getConfig()["basic"]["outputPath"]
        filename = path + "_".join(strList) + recEnv["fileType"]
        self._takeRecord(filename)
        logger.info("Generate filename {name}", name=filename)
        return filename

    def _takeRecord(self, filename: str):
        self.fileList.append(filename)


recorderGlobal = RecorderGlobal()
