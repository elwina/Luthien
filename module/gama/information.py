from core.typing.inputType import TYPE_Information
from core.typing.outputType import TYPE_Output_Information

MODULE_NAME: str = "gama"
MODULE_ROOT = "module/gama/"

MODULE_INSTANCE_INF: TYPE_Information = {
    "gamaUni": {
        "required": True,
    },
    "building": {
        "required": True,
    },
    "road": {
        "required": True,
    },
    "trips": {
        "required": True,
    },
}

MODULE_OUTPUT_INSTANCE_INF: TYPE_Output_Information = {"out": {}}
