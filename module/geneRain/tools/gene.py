from math import log10
from time import time
from pandas import DataFrame


def gene():
    # 芝加哥雨型
    A1, A2, B, C, r = 134.5106, 0.4784, 32.0692, 1.1947, 0.4

    totalMinutes = 180

    re = {}

    for P in [5, 8, 10, 15, 20, 50]:
        rains = []
        A = A1 * (1 + A2 * log10(P))
        for t in range(totalMinutes):
            if t <= float(r) * totalMinutes:
                t = totalMinutes / 2 - t
                val = 60 * A * ((1 - C) * t / r + B) / ((t / r + B)**(C + 1))
                rains.append(val)
            else:
                t = t - totalMinutes / 2
                val = 60 * A * ((1 - C) * t /
                                (1 - r) + B) / ((t / (1 - r) + B)**(C + 1))
                rains.append(val)
        re[str(P)] = rains

    df = DataFrame(re)
    df.to_csv("output/lab/rainraingene.csv")


gene()