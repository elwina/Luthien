from core.base.rasterType import TYPE_RASTER_DATA


def arrayRaster2Txt(dataset, outputRasterFile):
    band = dataset.GetRasterBand(1)
    reArr = band.ReadAsArray()

    (xllcorner, cellsize, _, oyllcorner, _,
     ycellsize) = dataset.GetGeoTransform()
    yllcorner = oyllcorner + ycellsize * reArr.shape[0]
    wdata = TYPE_RASTER_DATA(row=reArr.shape[0],
                             col=reArr.shape[1],
                             xllCorner=xllcorner,
                             yllCorner=yllcorner,
                             cellSize=cellsize,
                             nullData=band.GetNoDataValueAsInt64(),
                             radata=reArr)
    from core.tools.raster2Txt import raster2Txt
    raster2Txt(wdata, outputRasterFile)
