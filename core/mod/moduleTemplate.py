from typing import Sequence
from core.mod.inputManager import inputManager

from core.typing.moduleType import TYPE_Module


class ModuleTemplate(TYPE_Module):
    inputFieldsRequired: Sequence[str]

    def __init__(self, name):
        self.name = name
        self.inMr = inputManager()
