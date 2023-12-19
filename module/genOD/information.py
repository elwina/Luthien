from core.typing.inputType import TYPE_Information
from core.typing.outputType import TYPE_Output_Information

MODULE_NAME: str = "genOD"
MODULE_ROOT = "module/genOD/"

MODULE_INSTANCE_INF: TYPE_Information = {
    "genODUni": {
        "required": True,
    },
    "building": {
        "required": False,
    },
    "files": {
        "required": True,
    },
}

MODULE_OUTPUT_INSTANCE_INF: TYPE_Output_Information = {
    "ODTable": {},
    "ODJson": {},
    "TraceJson": {},
}
