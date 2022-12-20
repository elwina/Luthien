from typing_extensions import NotRequired, Required, TypedDict
from typing import Any, Mapping, MutableMapping, Sequence

from core.utils.confType import TYPE_CONF_VALUE


class TYPE_LIST_CONF_IN_A_DATA(TypedDict, total=False):
    name: Required[str]
    type: Required[str]
    default: TYPE_CONF_VALUE


TYPE_LIST_CONF_IN_DATA = Sequence[TYPE_LIST_CONF_IN_A_DATA]

TYPE_LIST_CONF_DATA = MutableMapping[str, TYPE_CONF_VALUE]
