from typing import Any, Literal, MutableMapping, MutableSequence, Sequence
from typing_extensions import TypedDict

TYPE_VECTOR_TYPE = Literal["Point", "MultiPoint", "LineString",
                           "MultiLineString", "Polygon", "MultiPolygon"]


class AVector:
    properties: MutableMapping[str, Any]
    coordinates: MutableSequence[MutableSequence[tuple[
        float, float]]] | MutableSequence[tuple[float, float]] | tuple[float,
                                                                       float]


class VectorData:
    type: TYPE_VECTOR_TYPE
    objects: MutableSequence[AVector]
