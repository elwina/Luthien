from loguru import logger
from core.typing.ioType import TYPE_IO_DATA
'''
config
    outRasterBase: # 用rasterbase中的data形式输出

    inFile:True # 以文件的形式输入配置
    inFilePath:"" # 文件路径
'''


def txt2RasterIO(ioData: TYPE_IO_DATA) -> TYPE_IO_DATA:
    config = ioData["config"]
    data = {}
    if "inFile" in config and config["inFile"] == True:
        filepath = config["inFilePath"]
        logger.info("Read Txt File {path}", path=filepath)
        
        with open(filepath) as fp:
            for _ in range(6):
                line = fp.readline()
                con = line.split()
                match con[0] :
                    case "nrows":
                        data["row"]=int(con[1])
                    case "ncols":
                        data["col"]=int(con[1])
                    case "cellsize":
                        data["cellSize"]=float(con[1])
                    case "NODATA_value":
                        data["nullData"]=float(con[1])
                    case "xllcorner":
                        data["xllCorner"]=float(con[1])
                    case "yllcorner":
                        data["yllCorner"]=float(con[1])

            rdata=[]
            lines = fp.readlines()
            for line in lines:
                con = line.split()
                if con.__len__()==0:
                    break
                if con.__len__()!=data["col"]:
                    logger.error("Col Number Wrong!")
                rdata.append(con)
 
            # 行校验
            trueRow=rdata.__len__()
            if trueRow !=data["row"]:
               logger.error("Row Number Wrong!")

            data["radata"]  =rdata

        # 简要报告
        logger.info("Read Done {path},row:{row},col:{col}",
                    path=filepath,row=data["row"],col=data["col"])

        if "outRasterBase" in config and config["outRasterBase"] == True:
            ioData["newData"]=data

    return ioData

if __name__ == "__main__":
    txt2RasterIO({
        "config": {
            "outRasterBase":True,
            "inFile": True,
            "inFilePath": "data/demtest.txt"
        },
        "oldData": None,
        "newData": None
    })