from typing import MutableMapping, Sequence, cast
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
    return streetDict


if __name__ == '__main__':
    filename = 'data/test165.net.xml'
    streetDict = extractStreet(filename)
    print(streetDict)