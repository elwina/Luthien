import sys
import commentjson as json

from core.typing.configType import Type_Config_Json

from config.path import CONFIG_JSON_PATH


class ConfigGlobal():
    filepath:str
    config: Type_Config_Json

    def __init__(self):
        self.filepath = CONFIG_JSON_PATH

    def getConfig(self) -> Type_Config_Json:
        '''获得配置'''
        return self.config

    def setConfig(self, filepath):
        '''更改配置文件路径'''
        self.filepath = filepath

    def initConfig(self):
        '''从文件中读取配置'''
        print(self.filepath)
        try:
            with open(self.filepath,encoding="utf-8") as fp:
                config: Type_Config_Json = json.load(fp)
            self.config = config
        except Exception as e:
            print(e)
            print("Config File Not Found!")
            print("Exit!")
            sys.exit(2)


configGlobal = ConfigGlobal()
