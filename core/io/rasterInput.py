from core.base.raster import Raster


def rasterInputZeros(raster: Raster):
    col = raster.col
    row = raster.row
    data = [[0 for i in range(col)] for j in range(row)]
    raster.data = data
