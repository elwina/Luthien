from typing import Dict, List, TypedDict, Literal, Any


class TYPE_Link_Declare(TypedDict):
    module: str
    input: Any
    output: Any


class TYPE_A_Link(TypedDict):
    module: str
    input: Any
    output: Any


class TYPE_Link_Json(TypedDict):
    version: int
    link: list[TYPE_A_Link]


_a: TYPE_Link_Json = {
    "version":
    1,
    "link": [{
        "module":
        "sample",
        "input": [{
            "var": "",
            "default": {
                "type": "",
                "value": ""
            },
            "predefine": {},
            "connect": {
                "type": "level",
                "content": []
            },
            "cover": {}
        }],
        "output": [{
            "var": ""
        }]
    }, {
        "input": [],
        "module": "sample2",
        "output": []
    }]
}