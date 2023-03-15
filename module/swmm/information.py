from core.typing.inputType import TYPE_Information
from core.typing.outputType import TYPE_Output_Information

MODULE_NAME: str = "swmm"
MODULE_ROOT = "module/swmm/"

MODULE_INSTANCE_INF: TYPE_Information = {
    "swmmUni": {
        "required": True,
    },
    "inpFile": {
        "required": True,
    },
    "rainFile": {
        "required": True
    }
}

MODULE_OUTPUT_INSTANCE_INF: TYPE_Output_Information = {"floodNode": {}}
