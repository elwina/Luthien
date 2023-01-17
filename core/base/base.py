from typing import Any, cast
from core.insTimeManager import InsTimeManager
from core.typing.fieldType import TYPE_Instance


class BaseBase:
    iTM:InsTimeManager

    def __init__(self):
        self.iTM=InsTimeManager(cast(Any,self))
        