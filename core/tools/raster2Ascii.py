import numpy as np
from osgeo import gdal, ogr, osr, gdalconst

from loguru import logger


def raster2Ascii(rasterfile: str, destfile: str):
    logger.info("Write raster txt {path}.", path=destfile)

    dataset = gdal.Open(rasterfile, gdalconst.GA_ReadOnly)
    band = dataset.GetRasterBand(1)
    array = band.ReadAsArray()

    (xllcorner, cellsize, _, oyllcorner, _, ycellsize) = dataset.GetGeoTransform()
    yllcorner = oyllcorner + ycellsize * array.shape[0]

    row = array.shape[0]
    col = array.shape[1]
    xllCorner = xllcorner
    yllCorner = yllcorner
    cellSize = cellsize
    nullData = band.GetNoDataValue()

    try:
        with open(destfile, "w") as fp:
            headstr = "ncols\t{ncols}\nnrows\t{nrows}\nxllcorner\t{xllcorner}\nyllcorner\t{yllcorner}\ncellsize\t{cellsize}\nNODATA_value\t{NODATA_value}".format(
                ncols=col,
                nrows=row,
                xllcorner=xllCorner,
                yllcorner=yllCorner,
                cellsize=cellSize,
                NODATA_value=nullData,
            )
            # fp.write(instr)

            np.savetxt(fp, array, fmt="%.1f", header=headstr, comments="")

            # dataList = list(
            #     map(
            #         lambda row: (" ".join(map(lambda x: str(x), row)) + "\n"),
            #         array,
            #     )
            # )

            # fp.writelines(dataList)
    except Exception as e:
        logger.error(e)
        logger.error("Cannot write raster txt.")
