import json
import math
import numpy as np
import pandas as pd


def actionGen(actionconf, config):
    trip = []

    def parseAction(action, agent: str, origin: str, id: list[int]):
        # 分配
        if action.__len__() == 0:
            return
        total = len(id)
        choicenum = []
        for act in action:
            p = int(act["p"]) / 100
            n = math.floor(total * p)
            choicenum.append(n)

        if sum(choicenum) < total:
            add = total - sum(choicenum)
            choicenum[-1] += add

        nowi = 0
        # 生成
        for i, act in enumerate(action):
            n = choicenum[i]
            [hour, minute] = act["time"].split(":")
            m = int(hour) * 60 + int(minute)
            startTime = np.random.normal(m, int(act["float"]) / 6, n)
            startTime = np.round(startTime)
            startTime = startTime.astype(int)
            idlist = []
            for j in range(n):
                time = "{}:{}".format(
                    str(startTime[j] // 60).zfill(2), str(startTime[j] % 60).zfill(2)
                )
                th = str(startTime[j] // 60)
                tm = str(startTime[j] % 60)
                trip.append(
                    {
                        "id": id[nowi],
                        "agent": agent,
                        "name": agent + str(id[nowi]),
                        "hour": th,
                        "minute": tm,
                        "o": origin,
                        "d": act["to"],
                    }
                )
                idlist.append(id[nowi])
                nowi += 1
            if "action" in act and act["action"].__len__() != 0:
                parseAction(act["action"], agent, act["to"], idlist)

    for agent in actionconf["detail"]:
        detail = actionconf["detail"][agent]
        idlist = [i for i in range(config[agent])]
        parseAction(detail["action"], agent, detail["init"], idlist)

    # with open("module/genOD/tools/sample.trip.json", "w", encoding="utf-8") as f:
    #     json.dump(trip, f, indent=2, ensure_ascii=False)

    # 生成一个人的图
    trace = {}
    for agent in actionconf["detail"]:
        for id in [i for i in range(config[agent])]:
            name = agent + str(id)
            trace[name] = [actionconf["detail"][agent]["init"]]
    for t in trip:
        trace[t["name"]].append(
            "".join(
                [
                    "/",
                    t["hour"].zfill(2),
                    ":",
                    t["minute"].zfill(2),
                    "--",
                    t["o"],
                    "--",
                    t["d"],
                ]
            )
        )
    for name in trace:
        trace[name] = "".join(trace[name])
    # with open("module/genOD/tools/sample.trace.json", "w", encoding="utf-8") as f:
    #     json.dump(trace, f, indent=2, ensure_ascii=False)

    return trip, trace


# with open("module/genOD/tools/sample.action.json", "r", encoding="utf-8") as f:
#     action = json.load(f)

# with open("module/genOD/tools/sample.config.json", "r", encoding="utf-8") as f:
#     config = json.load(f)

# actionGen(action, config)
