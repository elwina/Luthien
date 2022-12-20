from typing import Any, MutableMapping, Sequence

from loguru import logger
from core.typing.outputType import TYPE_Output_Information, TYPE_Putout
from core.typing.recordType import TYPE_A_Record

from core.env import env
'''
inf{
    out1:{}
}

putout
{
    out1:{
        0:instance
        1
        2
        3....
    }
}
'''
'''
instances
{
    absoulteTime:{
        out1:instance
    }
}
'''
'''
校准时间
'''


class outputManager:
    information: TYPE_Output_Information = {}
    instances: MutableMapping[int, MutableMapping[str, Any]]

    def __init__(self):
        pass

    def init(self, inf: TYPE_Output_Information):
        self.information = inf
        self.instances = {}

    def getTimenow(self):
        return env.epoch

    def clearCache(self):
        self.instances = dict(
            filter(lambda x: x[0] >= self.getTimenow(),
                   self.instances.items()))

    def check(self, name: str, time: int):
        if time in self.instances:
            if name in self.instances[time]:
                return True
        return False

    def putout(self, data: TYPE_Putout):
        for name in data:
            for rtime in data[name]:
                ins = data[name][rtime]
                atime = self.getTimenow() + rtime
                if atime not in self.instances:
                    self.instances[atime] = {}
                self.instances[atime][name] = ins

    def getOutput(self, name: str, time: int):
        if self.check(name, time):
            return self.instances[time][name]
        else:
            logger.error("A output not found,name:{name},time{time}",
                         name=name,
                         time=time)
            return None

    def makeRecords(self, recordList: Sequence[TYPE_A_Record]):
        '''记录'''
        for record in recordList:
            self.recordIns(record["catch"], record["method"], record["config"])

    def recordIns(self, name, methodName: str, config: MutableMapping[str,
                                                                      Any]):
        ins = self.instances[self.getTimenow()][name]
        from config.register import RECORDER_LIST
        method = RECORDER_LIST[methodName]
        method({
            "config": config,
            "data": ins.data,
            "tempEnv": {
                "insName": name,
                "ifModule": True,
                "linkDes": str(env.linkNowNum)
            }
        })
