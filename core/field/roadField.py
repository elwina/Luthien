from core.typing.fieldType import TYPE_Field

from core.base.vector import VectorBase


class RoadField(VectorBase, TYPE_Field):
    '''内置Field:路网'''

    def __init__(self):
        super().__init__("road")
        self.init("MultiLineString")
