from core.typing.fieldType import TYPE_Field

from core.base.vector import VectorBase


class RoadField(VectorBase, TYPE_Field):
    '''内置Field:路网'''

    def __init__(self):
        super().__init__("road")
        self.init("MultiLineString")

    def getAStreet(self, name: str):
        return self.getInsByOneProp("name", name)

    def getAllStreets(self):
        streets:list[str]=list(set(list(map(lambda aVec:aVec.properties.get("name","NONAME"),self.data.objects))))
        return streets