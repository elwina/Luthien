from core.typing.fieldType import TYPE_Field

from core.base.vector import VectorBase


class NodesField(VectorBase, TYPE_Field):
    """内置Field:节点"""

    def __init__(self):
        super().__init__("nodes")
        self.init("Point")
