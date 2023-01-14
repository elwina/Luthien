from typing import Any, MutableMapping, MutableSequence, TypedDict


class TYPE_RASTER_DATA(TypedDict):
    row: int
    col: int
    cellSize: float
    nullData: float
    xllCorner: float
    yllCorner: float
    radata: MutableSequence[MutableSequence[float | float]]
