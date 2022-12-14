from typing import Dict, List, TypedDict, Literal, Any


class _TYPE_A_Link(TypedDict):
    module: str
    input: Any
    output: Any


class TYPE_Link_Json(TypedDict):
    version: int
    link: list[_TYPE_A_Link]


a: TYPE_Link_Json = {
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