from typing import Any, MutableMapping, Sequence

from loguru import logger
#from config.register import RECORDER_LIST
from core.typing.outputType import TYPE_Output_Information, TYPE_Putout
from core.typing.recordType import TYPE_A_Record, TYPE_Recorder_Env
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

    timenow: int

    def __init__(self):
        pass

    def init(self, inf: TYPE_Output_Information):
        self.information = inf
        self.clearCache()

    def setTime(self, time: int):
        self.timenow = time

    def clearCache(self):
        self.instances = {}

    def check(self, name: str, time: int):
        if time in self.instances:
            if name in self.instances[time]:
                return True
        return False

    def putout(self, data: TYPE_Putout):
        for name in data:
            for rtime in data[name]:
                ins = data[name][rtime]
                atime = self.timenow + rtime
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

    def makeRecords(self, recordList: Sequence[TYPE_A_Record],
                    env: TYPE_Recorder_Env):
        '''记录'''
        for record in recordList:
            self.recordIns(record["catch"], record["method"], record["config"],
                           env)

    def recordIns(self, name, methodName: str,
                  config: MutableMapping[str, Any], env: TYPE_Recorder_Env):
        ins = self.instances[0][name]
        method = RECORDER_LIST[methodName]
        env["pre"] = env["pre"] + "inside-" + name
        method({"config": config, "data": ins.data, "env": env})
