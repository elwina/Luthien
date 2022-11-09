from core.base.raster import Raster


class DemField(Raster):

    def __init__(self, row, col, cellSize, nullData=-9999):
        super(DemField, self).__init__("DEM")
