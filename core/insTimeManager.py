from asyncio import Protocol
from copy import deepcopy
from typing import Any, Generic, MutableMapping,TypeVar

from core.envGlobal import envGlobal

class _TYPE_Field_Local(Protocol):
    data:Any

class InsTimeManager():
    ins: _TYPE_Field_Local
    keyframe: MutableMapping[int, Any]

    def __init__(self, ins: _TYPE_Field_Local):
        self.ins = ins
        self.keyframe = {}

    def store(self, keyframe: MutableMapping[int, Any]):
        keyframe = deepcopy(keyframe)
        self.keyframe.update(keyframe)

    def storeRel(self, relKeyframe: MutableMapping[int, Any]):
        timenow = envGlobal.epoch
        keyframe = dict(
            zip(map(lambda t: t + timenow, relKeyframe.keys()),
                relKeyframe.values()))
        self.store(keyframe)

    def jumpTime(self, time: int):
        if time in self.keyframe:
            self.ins.data = deepcopy(self.keyframe[time])
        else:
            time = time - 1

    def checkTime(self):
        timenow = envGlobal.epoch
        if timenow in self.keyframe:
            self.ins.data = deepcopy(self.keyframe[timenow])

    def getTimeIns(self, time: int):
        ins = deepcopy(self.ins)
        if time in self.keyframe:
            ins.data = deepcopy(self.keyframe[time])
        else:
            time = time - 1
        return ins

    def getKeyframe(self):
        time=envGlobal.epoch
        return list(filter(lambda t:t>=time,self.keyframe.keys()))
    
    def geneKeyFrame(self):
        for time in self.getKeyframe():
            self.jumpTime(time)
            yield time,self.ins
        self.checkTime()