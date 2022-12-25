from typing import Any, MutableMapping, Sequence, TypedDict


class TYPE_RASTER_DATA(TypedDict):
    row: int
    col: int
    cellSize: float
    nullData: float
    xllCorner: float
    yllCorner: float
    radata: Sequence[Sequence[float | float]]
