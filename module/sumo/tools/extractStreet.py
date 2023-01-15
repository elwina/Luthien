import os
import sys
from typing import MutableMapping, MutableSequence, Sequence, cast
import xml.etree.ElementTree as ET

TYPE_Street_Dict = MutableMapping[str, list[str]]


def extractStreet(filename: str) -> TYPE_Street_Dict:
    '''
    从sumo生成的xml文件中提取steet信息
    '''
    tree = ET.parse(filename)
    root = tree.getroot()
    edges = root.findall('edge')
    streetDict: TYPE_Street_Dict = {}
    for edge in edges:
        name = edge.attrib.get('name')
        if name is not None:
            if streetDict.get(name) is None:
                streetDict[name] = []
            id = cast(str, edge.attrib.get('id'))
            streetDict[name].append(id)
        else:
            if streetDict.get('NONAME') is None:
                streetDict['NONAME'] = []
            id = cast(str, edge.attrib.get('id'))
            streetDict['NONAME'].append(id)
    return streetDict


def extractStreet2MultiLineString(filename: str):
    '''
    从sumo生成的xml文件中提取steet信息
    '''
    origin=sys.path.copy()
    if 'SUMO_HOME' in os.environ:
        sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
    import sumolib
    sys.path=origin

    net = sumolib.net.readNet(filename)
    convert = net.convertXY2LonLat

    from core.field.roadField import RoadField
    from core.base.vector import VectorData, AVector
    road = RoadField()
    data = VectorData()
    data.type = "MultiLineString"
    data.objects = []

    street = extractStreet(filename)
    newObj: MutableMapping[str, AVector] = {}
    for sname in street.keys():
        adata = AVector()
        adata.properties = {'name': sname, 'lanes': [], 'edges': []}
        adata.coordinates = []
        newObj[sname] = adata

    tree = ET.parse(filename)
    root = tree.getroot()
    edges = root.findall('edge')

    for edge in edges:
        if edge.attrib.get('function') == 'internal':
            continue
        name = edge.attrib.get('name')
        if name is None:
            name = 'NONAME'

        edgeid = cast(str, edge.attrib.get('id'))
        newObj[name].properties['edges'].append(edgeid)

        for lane in edge.findall('lane'):
            laneid = cast(str, lane.attrib.get('id'))
            newObj[name].properties['lanes'].append(laneid)

        fromjuction = edge.attrib.get('from')
        tojuction = edge.attrib.get('to')

        frompos = []
        topos = []

        if root.find(f'junction[@id="{fromjuction}"]') is not None:
            j = cast(ET.Element, root.find(f'junction[@id="{fromjuction}"]'))
            x = j.attrib.get('x')
            y = j.attrib.get('y')
            if x is not None and y is not None:
                frompos = [(float(x), float(y))]

        if root.find(f'junction[@id="{tojuction}"]') is not None:
            j = cast(ET.Element, root.find(f'junction[@id="{tojuction}"]'))
            x = j.attrib.get('x')
            y = j.attrib.get('y')
            if x is not None and y is not None:
                topos = [(float(x), float(y))]

        shapepos = []
        shape = edge.attrib.get('shape')
        if shape is not None:
            for pos in shape.split(' '):
                x = pos.split(',')[0]
                y = pos.split(',')[1]
                if x is not None and y is not None:
                    shapepos.append((float(x), float(y)))
        coo: MutableSequence[tuple[float, float]] = frompos + shapepos + topos
        coo = [convert(x, y) for x, y in coo]

        cast(MutableSequence[MutableSequence[tuple[float, float]]],
             newObj[name].coordinates).append(coo)

    data.objects = list(newObj.values())
    road.data = data
    return road


if __name__ == '__main__':
    filename = 'data/test165.net.xml'
    road = extractStreet2MultiLineString(filename)
    print(road.getTempFile())