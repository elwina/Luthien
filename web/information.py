from dataclasses import Field
import json
import os


def getInf():
    inf = {}
    inf["module"] = []

    from config.register import MODULE_LIST,FIELD_LIST, IO_LIST, RECORDER_LIST
    for (name, Mo) in MODULE_LIST.items():
        m = Mo()
        moInf = {"name": name, "input": m.inInf, "output": m.outInf}
        inf["module"].append(moInf)

    inf["IO"] = list(IO_LIST.keys())
    inf["Recorder"] = list(RECORDER_LIST.keys())
    inf["Field"]=list(FIELD_LIST.keys())

    jsonpath = "web/configui/src/information.json"
    with open(jsonpath, 'w') as f:
        json.dump(inf, f, ensure_ascii=False)
