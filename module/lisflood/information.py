from core.typing.inputType import TYPE_Information
from core.typing.outputType import TYPE_Output_Information

MODULE_NAME: str = "lisflood"
MODULE_ROOT = "module/lisflood/"

MODULE_INSTANCE_INF: TYPE_Information = {
    "dem": {
        "required": True
    },
    "lisUni": {
        "required": True
    },
    "addFiles": {
        "required": False
    },
    "pointXY": {
        "required": False
    },
    "pointWater": {
        "required": False
    }
}

MODULE_OUTPUT_INSTANCE_INF: TYPE_Output_Information = {
    "water": {},
    "files": {}
}
