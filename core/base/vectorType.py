from typing import Any, Generic, Literal, MutableMapping, MutableSequence, Sequence, TypeVar
from typing_extensions import TypedDict

TYPE_VECTOR_TYPE = Literal["Point", "MultiPoint", "LineString",
                           "MultiLineString", "Polygon", "MultiPolygon"]

TYPE_COO_SST=MutableSequence[MutableSequence[tuple[
        float, float]]]
TYPE_COO_ST=MutableSequence[tuple[float, float]]
TYPE_COO_T=tuple[float, float]
TYPE_COO=TYPE_COO_SST|TYPE_COO_ST|TYPE_COO_T


class AVector():
    properties: MutableMapping[str, Any]
    coordinates: TYPE_COO_SST | TYPE_COO_ST | TYPE_COO_T


class VectorData:
    type: TYPE_VECTOR_TYPE
    objects: MutableSequence[AVector]
