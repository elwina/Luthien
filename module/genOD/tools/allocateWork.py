from copy import deepcopy
import numpy as np


def allocateWork(trip, config, place):
    # place = {work: [place1, place2, ...], ...}
    allsubs = {}
    for work in place:
        allsubs[work] = {}
        places = place[work]
        for agent in config:
            num = config[agent]
            choices = np.random.choice(places, num)
            allsubs[work][agent] = choices

    newTrip = deepcopy(trip)
    # try:
    for t in newTrip:
        agent = t["agent"]
        id = t["id"]

        t["o"] = int(allsubs[t["o"]][agent][id])
        t["d"] = int(allsubs[t["d"]][agent][id])

    return newTrip
    # except:
    #     raise Exception("Error in allocateWork")
