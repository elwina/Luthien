import os
import uuid

from typing import cast
from core.base.rasterType import TYPE_RASTER_DATA
from core.typing.ioType import TYPE_IO_Data

from loguru import logger
from osgeo import gdal, ogr, osr, gdalconst

'''
config
    outRasterBase: #* 用rasterbase中的data形式输出

    inFilePath:"" #* 文件路径
    inDriver:"" ["AAIGrid","GTiff"]

'''


def txt2RasterIO(ioData: TYPE_IO_Data) -> TYPE_IO_Data:
    from core.base.raster import RasterBase
    config = ioData["config"]
    ins: RasterBase = ioData["ins"]
    data = TYPE_RASTER_DATA()

    if config.get("inDriver") == "AAIGrid":
        filepath = config["inFilePath"]
        logger.info("Read Txt File {path}", path=filepath)
        
        try:
            with open(filepath,encoding="utf-8") as fp:
                for _ in range(6):
                    line = fp.readline()
                    con = line.split()
                    match con[0] :
                        case "nrows":
                            data.row=int(con[1])
                        case "ncols":
                            data.col=int(con[1])
                        case "cellsize":
                            data.cellSize=float(con[1])
                        case "NODATA_value":
                            data.nullData=float(con[1])
                        case "xllcorner":
                            data.xllCorner=float(con[1])
                        case "yllcorner":
                            data.yllCorner=float(con[1])

                rdata=[]
                lines = fp.readlines()
                for line in lines:
                    con = line.split()
                    if con.__len__()==0:
                        break
                    if con.__len__()!=data.col:
                        logger.error("Col Number Wrong!")
                    rdata.append(list(map(lambda x:float(x),con)))
    
                # 行校验
                trueRow=rdata.__len__()
                if trueRow !=data.row:
                    logger.error("Row Number Wrong!")

                data.radata  =rdata

        except Exception as e:
            logger.error(e)
            logger.error("Raster file wrong!")

        # 简要报告
        logger.trace("Read Done {path},row:{row},col:{col}",
                    path=filepath,row=data.row,col=data.col)
    elif config.get("inDriver") == "GTiff":
        filepath = config["inFilePath"]
        ds = gdal.Open(filepath, gdalconst.GA_ReadOnly)
        from core.tools.gdal2Txt import arrayRaster2Txt
        outputFile=os.path.join("temp",str(uuid.uuid4())+"raster.txt")
        arrayRaster2Txt(ds,outputFile)
        data = readAscii(outputFile)
    else:
        logger.warning("No driver inputed in config.")
        filepath = config["inFilePath"]
        ds = gdal.Open(filepath, gdalconst.GA_ReadOnly)
        from core.tools.gdal2Txt import arrayRaster2Txt
        outputFile=os.path.join("temp",str(uuid.uuid4())+"raster.txt")
        arrayRaster2Txt(ds,outputFile)
        data = readAscii(outputFile)
        

    if "outRasterBase" in config and config["outRasterBase"] == True:
        ioData["newData"]=data
        ins.data=data

    return ioData

def readAscii(filepath:str): 
    data = TYPE_RASTER_DATA()   
    with open(filepath,encoding="utf-8") as fp:
        for _ in range(6):
            line = fp.readline()
            con = line.split()
            match con[0] :
                case "nrows":
                    data.row=int(con[1])
                case "ncols":
                    data.col=int(con[1])
                case "cellsize":
                    data.cellSize=float(con[1])
                case "NODATA_value":
                    data.nullData=float(con[1])
                case "xllcorner":
                    data.xllCorner=float(con[1])
                case "yllcorner":
                    data.yllCorner=float(con[1])

        rdata=[]
        lines = fp.readlines()
        for line in lines:
            con = line.split()
            if con.__len__()==0:
                break
            if con.__len__()!=data.col:
                logger.error("Col Number Wrong!")
            rdata.append(list(map(lambda x:float(x),con)))

        # 行校验
        trueRow=rdata.__len__()
        if trueRow !=data.row:
            logger.error("Row Number Wrong!")

        data.radata  =rdata


    # 简要报告
    logger.trace("Read Done {path},row:{row},col:{col}",
                path=filepath,row=data.row,col=data.col)
    
    return data
