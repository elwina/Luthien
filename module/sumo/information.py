from core.typing.inputType import TYPE_Information
from core.typing.outputType import TYPE_Output_Information

MODULE_NAME: str = "sumo"
MODULE_ROOT = "module/sumo/"

MODULE_INSTANCE_INF: TYPE_Information = {
    "uniSumo": {
        "required": True,
    },
    "network": {
        "required": True
    },
    "routeFiles": {
        "required": False
    }
}

MODULE_OUTPUT_INSTANCE_INF: TYPE_Output_Information = {"files": {}}
