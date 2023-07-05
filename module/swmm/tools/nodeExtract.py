from typing import MutableSequence, cast
import numpy

from core.base.vectorType import TYPE_COO_T


def nodeExtract(filepath: str):
    from module.swmm.field.drainPointField import DrainPointField
    from core.base.vectorType import AVector

    field = DrainPointField()
    objs: MutableSequence[AVector] = []

    path = filepath
    outfalls = getType(path, "[OUTFALLS]")
    junctions = getType(path, "[JUNCTIONS]")

    with open(path, mode="r", encoding="utf-8") as fp:
        ifIn = False
        while True:
            line = fp.readline()
            if not line:
                break
            str = line.strip()
            if str.__len__() == 0:
                continue
            if str[0] == ";":
                continue

            if ifIn == True and str[0] == "[":
                break

            if ifIn == True:
                arr = str.split(None)
                arr = list(filter(None, arr))
                [nodeid, cooX, cooY] = arr
                cooX = float(cooX)
                cooY = float(cooY)

                av = AVector()
                av.properties = {}

                av.properties["nodeid"] = nodeid

                if nodeid in junctions:
                    av.properties["type"] = "junction"
                if nodeid in outfalls:
                    av.properties["type"] = "outfall"

                av.coordinates = (cooX, cooY)
                objs.append(av)

            if str == "[COORDINATES]":
                ifIn = True
            else:
                continue
    field.data.objects = objs
    path = field.getTempFile()

    # pointArray = list(map(lambda obj: obj.coordinates, objs))
    # pointArray = cast(list[TYPE_COO_T], pointArray)
    # npPoints=numpy.array(pointArray)
    # vor = Voronoi(npPoints)

    # import matplotlib.pyplot as plt

    print(path)
    return field


def getType(filepath: str, find="[OUTFALLS]"):
    re = []
    with open(filepath, mode="r", encoding="utf-8") as fp:
        ifIn = False
        while True:
            line = fp.readline()
            if not line:
                break
            str = line.strip()

            if str.__len__() == 0:
                continue

            if str[0] == ";":
                continue

            if ifIn == True and str[0] == "[":
                break

            if ifIn == True:
                arr = str.split(None)
                arr = list(filter(None, arr))
                name = arr[0]
                re.append(name)

            if str == find:
                ifIn = True
            else:
                continue
    return re
