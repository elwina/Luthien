from typing import MutableMapping

from loguru import logger


def dict2Txt(data: MutableMapping, filename: str):
    logger.info("Write dict txt {path}.", path=filename)
    string: str = "\n".join(map(lambda x: x + "\t" + str(data[x]), data))
    try:
        with open(filename, "w") as fp:
            fp.write(string)
    except Exception as e:
        logger.error(e)
        logger.error("Cannot write dict into txt.")