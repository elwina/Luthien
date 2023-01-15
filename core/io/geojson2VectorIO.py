from core.typing.ioType import TYPE_IO_Data
'''
config
    outVectorBase: bool

    inFile: bool
    inFilePath: str
    intype: str
'''


def geojson2VectorIO(ioData: TYPE_IO_Data) -> TYPE_IO_Data:
    from core.base.vector import VectorBase

    config = ioData["config"]
    ins: VectorBase = ioData["ins"]
    data = {}
    if "inFile" in config and config["inFile"] == True:
        filepath = (config["inFilePath"])

    if "outVectorBase" in config and config["outVectorBase"] == True:
        pass
    return ioData