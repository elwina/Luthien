from core.typing.ioType import TYPE_IO_Data
'''
config
    outVectorBase: bool

    inFile: bool
    inFilePath: str
    intype: str
'''


def geojson2VectorIO(ioData: TYPE_IO_Data) -> TYPE_IO_Data:
    config = ioData["config"]
    oldData = ioData["oldData"]
    data = {}
    if "inFile" in config and config["inFile"] == True:
        filepath=(config["inFilePath"])


    if "outListConf" in config and config["outListConf"] == True:
        for name in data:
            oldData[name] = data[name]
        ioData["newData"] = oldData
    return ioData