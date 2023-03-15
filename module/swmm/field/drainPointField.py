from core.typing.fieldType import TYPE_Field

from core.base.vector import VectorBase


class DrainPointField(VectorBase, TYPE_Field):
    '''Field:排水点与集水点'''

    def __init__(self):
        super().__init__("road")
        self.init("Point")

