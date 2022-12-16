from core.base.raster import RasterBase
from core.typing.fieldType import TYPE_Field


class DemField(RasterBase, TYPE_Field):

    def __init__(self):
        super(DemField, self).__init__("DEM")
        self.init()


if __name__ == "__main__":
    a = DemField()
    print(a.data)