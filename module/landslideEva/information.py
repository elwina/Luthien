from core.typing.inputType import TYPE_Information
from core.typing.outputType import TYPE_Output_Information

MODULE_NAME: str = "landslideEva"
MODULE_ROOT = "module/landslideEva/"

MODULE_INSTANCE_INF: TYPE_Information = {
    "water": {
        "required": True
    },
    "lanUni": {
        "required": False
    }
}

MODULE_OUTPUT_INSTANCE_INF: TYPE_Output_Information = {"eva": {}}
