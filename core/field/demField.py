from core.base.raster import RasterBase


class DemField(RasterBase):

    def __init__(self):
        super(DemField, self).__init__("DEM")
