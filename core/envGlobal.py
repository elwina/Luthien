from typing import Any


class _EnvGlobal:
    configPath: str = ""

    ct: Any

    timestep: int
    timeUnit: str
    allEpoches: int

    epoch: int

    moduleNow: str

    linkNowNum: int


envGlobal = _EnvGlobal()
