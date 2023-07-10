from core.typing.fieldType import TYPE_Field

from core.base.raster2 import RasterBase


class WaterField(RasterBase, TYPE_Field):
    """内置Field:水相关栅格模型"""

    def __init__(self):
        super(WaterField, self).__init__("rain")
        self.init()
