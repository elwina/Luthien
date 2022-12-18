from core.base.raster import RasterBase
from core.typing.fieldType import TYPE_Field


class RainField(RasterBase, TYPE_Field):

    def __init__(self):
        super(RainField, self).__init__("rain")
        self.init()
