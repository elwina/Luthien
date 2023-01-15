import os

from core.typing.inputType import TYPE_Information
from core.typing.outputType import TYPE_Output_Information

MODULE_NAME: str = "sumoSpeed"
MODULE_ROOT = os.path.join("module","sumoSpeed")

MODULE_INSTANCE_INF: TYPE_Information = {
    "water": {
        "required": True
    },
    "sumoSpeedUni": {
        "required": True
    },
    "road":{
        "required":True
    },
    "sumoNet": {
        "required": False
    }
}

MODULE_OUTPUT_INSTANCE_INF: TYPE_Output_Information = {"xml": {}}
