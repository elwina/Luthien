'''控制时间
always
once
a0-1-3从0开始每1跑一次直到3
a0-1从0开始每1跑一次
b0-1-2-3-4列举跑的时间
'''


def parseTime(ts: str, allEpoches=0) -> list:
    if allEpoches == 0:
        from core.envGlobal import envGlobal
        allEpoches = envGlobal.allEpoches

    if ts == "always":
        return list(range(allEpoches))

    if ts == "once":
        return [0]

    if ts.startswith("a"):
        tss = ts[1:]
        arr=tss.split("-")
        if len(arr)==2:
            start, step = tss.split("-")
            start = int(start)
            step = int(step)
            end=allEpoches
        else:
            start, step, end = tss.split("-")
            start = int(start)
            step = int(step)
            end = int(end)
        return list(range(start, end + 1, step))

    if ts.startswith("b"):
        tss = ts[1:]
        arr=tss.split("-")
        return list(map(int, arr))

    return list(range(allEpoches))

def ifTimeRun(ts: str, timenow: int=-1) -> bool:
    '''返回是否需要跑'''
    if timenow == -1:
        from core.envGlobal import envGlobal
        timenow = envGlobal.epoch
    return timenow in parseTime(ts)
