from dataclasses import dataclass, field
from typing import Any, MutableMapping, MutableSequence, Sequence, TypedDict


@dataclass
class TYPE_RASTER_DATA:
    row: int = 0
    col: int = 0
    cellSize: float = 0
    nullData: float = 0
    xllCorner: float = 0
    yllCorner: float = 0
    radata: Sequence[MutableSequence[float | int]] = field(default_factory=list)
