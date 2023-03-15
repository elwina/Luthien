import math
from typing import cast
from core.base.json import JsonBase
from core.base.vector import VectorBase
from core.base.vectorType import TYPE_COO_T


def getBciBdy(vField: VectorBase, pointWater: JsonBase):
    bdy = []
    bci = []

    for node, floods in pointWater.data.items():
        if math.isclose(sum(floods), 0.0):
            continue
        else:
            n = vField.getObjByOnePropNew("nodeid", node)
            lenn=floods.__len__()
            if n is None: continue
            x, y = cast(TYPE_COO_T, n.coordinates)
            bdy.append(f"P\t{x}\t{y}\tQVAR\t{node}\n")
            bcistr=list(map(lambda a:"%.6f\t%d\n"%(a[1],a[0]),enumerate(floods)))
            bci.append(f"{node}\n{lenn}\thours\n{bcistr}")
    
    return bci,bdy
