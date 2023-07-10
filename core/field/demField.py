from core.typing.fieldType import TYPE_Field

from core.base.raster2 import RasterBase


class DemField(RasterBase, TYPE_Field):
    """内置Field:高程图"""

    def __init__(self):
        super(DemField, self).__init__("dem")
        self.init()
