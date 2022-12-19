from loguru import logger


def raster2Txt(rasterData, filename: str):
    logger.info("Write Raster Txt {path}", path=filename)
    with open(filename, 'w') as fp:
        instr = "ncols\t{ncols}\nnrows\t{nrows}\nxllcorner\t{xllcorner}\nyllcorner\t{yllcorner}\ncellsize\t{cellsize}\nNODATA_value\t{NODATA_value}\n".format(
            ncols=rasterData['col'],
            nrows=rasterData['row'],
            xllcorner=rasterData['xllCorner'],
            yllcorner=rasterData['yllCorner'],
            cellsize=rasterData['cellSize'],
            NODATA_value=rasterData['nullData'])
        fp.write(instr)

        dataList = list(
            map(lambda row: (" ".join(map(lambda x: str(x), row)) + "\n"),
                rasterData['radata']))
        dataList[-1] = dataList[-1][:-1]
        fp.writelines(dataList)