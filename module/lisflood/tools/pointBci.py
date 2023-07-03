import math
from typing import cast
from core.base.json import JsonBase
from core.base.vector import VectorBase
from core.base.vectorType import TYPE_COO_T


def getBciBdy(vField: VectorBase, pointWater: JsonBase,cellsize:float):
    bdy = []
    bci = []

    for node, floods in pointWater.data.items():
        if math.isclose(sum(floods), 0.0):
            continue
        else:
            n = vField.getObjByOnePropNew("nodeid", node)
            lenn = floods.__len__()
            if n is None: continue
            x, y = cast(TYPE_COO_T, n.coordinates)
            bci.append(f"P\t{x}\t{y}\tQVAR\t{node}\n")
            bdystr = list(
                map(lambda a: "%.6f\t%d\n" % (a[1] / cellsize, a[0] * 60),
                    enumerate(floods)))
            bdystr = "".join(bdystr)
            bdy.append(f"{node}\n{lenn}\tseconds\n{bdystr}")

    return bci, bdy
