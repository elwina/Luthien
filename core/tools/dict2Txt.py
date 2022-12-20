from typing import MutableMapping

from loguru import logger


def dict2Txt(data: MutableMapping, filename: str):
    logger.info("Write Dict Txt {path}", path=filename)
    string: str = "\n".join(map(lambda x: x + "\t" + str(data[x]), data))
    with open(filename, "w") as fp:
        fp.write(string)