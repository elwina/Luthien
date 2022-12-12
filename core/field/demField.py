from core.base.raster import RasterBase


class DemField(RasterBase):

    def __init__(self, row, col, cellSize, nullData=-9999):
        super(DemField, self).__init__("DEM")
