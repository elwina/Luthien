from typing import Any, Literal, MutableMapping, MutableSequence, Sequence
from typing_extensions import TypedDict

TYPE_VECTOR_TYPE = Literal["Point","MultiPoint","LineString","MultiLineString","Polygon","MultiPolygon"]

class TYPE_A_VECTOR(TypedDict):
    properties: MutableMapping[str, Any]
    coordinates: MutableSequence[Sequence[float]] | Sequence[float]

class TYPE_VECTOR_DATA(TypedDict):
    type: TYPE_VECTOR_TYPE
    objects: MutableSequence[TYPE_A_VECTOR]
