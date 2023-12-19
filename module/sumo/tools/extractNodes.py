import os
import sys
from typing import MutableMapping
import xml.etree.ElementTree as ET


def extractNodes(filename: str):
    origin = sys.path.copy()
    if "SUMO_HOME" in os.environ:
        sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools"))
    import sumolib

    sys.path = origin

    net = sumolib.net.readNet(filename)
    convert = net.convertXY2LonLat

    from core.field.nodesField import NodesField
    from core.base.vectorType import VectorData, AVector

    nodesF = NodesField()
    data = VectorData()
    data.type = "Point"
    data.objects = []
    newObj: MutableMapping[str, AVector] = {}

    nodes = net.getNodes()
    for node in nodes:
        id = node.getID()
        newObj[id] = AVector()
        newObj[id].properties = {"id": id}

        x, y = node.getCoord()
        x, y = convert(x, y)
        newObj[id].coordinates = [x, y]

    data.objects = list(newObj.values())
    nodesF.data = data

    return nodesF


if __name__ == "__main__":
    filename = "data/ngz/sz.net.xml"
    node = extractNodes(filename)
    node.trans2Proj(4326, 32650)
    with open("output/test2/node.geojson", "w", encoding="utf-8") as f:
        f.write(node.toGeoJSONString())
