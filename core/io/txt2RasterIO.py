from core.typing.ioType import TYPE_IO_DATA

from loguru import logger
'''
config
    outRasterBase: #* 用rasterbase中的data形式输出

    inFile:True #* 以文件的形式输入配置
    inFilePath:"" #* 文件路径
'''


def txt2RasterIO(ioData: TYPE_IO_DATA) -> TYPE_IO_DATA:
    config = ioData["config"]
    data = {}
    if "inFile" in config and config["inFile"] == True:
        filepath = config["inFilePath"]
        logger.info("Read Txt File {path}", path=filepath)
        
        try:
            with open(filepath,encoding="utf-8") as fp:
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
                    rdata.append(list(map(lambda x:float(x),con)))
    
                # 行校验
                trueRow=rdata.__len__()
                if trueRow !=data["row"]:
                    logger.error("Row Number Wrong!")

                data["radata"]  =rdata

        except Exception as e:
            logger.error(e)
            logger.error("Raster file wrong!")

        # 简要报告
        logger.success("Read Done {path},row:{row},col:{col}",
                    path=filepath,row=data["row"],col=data["col"])

        if "outRasterBase" in config and config["outRasterBase"] == True:
            ioData["newData"]=data

    return ioData
