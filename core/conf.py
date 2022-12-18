from typing import MutableMapping
import commentjson as json
from config.path import CONFIG_JSON_PATH
from core.typing.configType import Type_Config_Json


# 获得配置
def getConfig() -> Type_Config_Json:
    filepath = CONFIG_JSON_PATH
    with open(filepath) as fp:
        config = json.load(fp)
    return config