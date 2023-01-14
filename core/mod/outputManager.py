from typing import Any, MutableMapping, MutableSequence
from core.typing.outputType import TYPE_Output_Information, TYPE_Putout
from core.typing.recordType import TYPE_Record_Declare

from loguru import logger
from core.envGlobal import envGlobal


class outputManager:
    information: TYPE_Output_Information = {}
    '''
    TYPE_Output_Information形如
    {water:{}}
    暂时无作用,备用
    '''

    instances: MutableMapping[int, MutableMapping[str, Any]]
    '''
    instances形如
    {
        absoulteTime:{
            out1:instance
        }
    }
    '''

    def __init__(self):
        pass

    def init(self, inf: TYPE_Output_Information):
        self.information = inf
        self.instances = {}

    def _getTimenow(self):
        return envGlobal.epoch

    def clearCache(self):
        '''清除缓存的函数,备用'''
        self.instances = dict(
            filter(lambda x: x[0] >= self._getTimenow(),
                   self.instances.items()))

    def _check(self, name: str, time: int):
        if time in self.instances:
            if name in self.instances[time]:
                return True
        return False

    def putout(self, data: TYPE_Putout):
        '''
        data形如
        {
            out1:{
                0:instance,
                1:instance
            }
        }
        数字代表相对时间
        '''
        for name in data:
            for rtime in data[name]:
                ins = data[name][rtime]
                atime = self._getTimenow() + rtime
                if atime not in self.instances:
                    self.instances[atime] = {}
                self.instances[atime][name] = ins

    def getOutput(self, name: str, time: int):
        '''获得output根据名称和绝对时间'''
        if self._check(name, time):
            return self.instances[time][name]
        else:
            logger.error("A output not found,name:{name},time:{time}.",
                         name=name,
                         time=time)
            return None

    def makeRecords(self, recordList: MutableSequence[TYPE_Record_Declare]):
        '''记录'''
        for record in recordList:
            self.recordIns(record["catch"], record["method"], record["config"])
        logger.success("Sucessfully make records in outMr.")

    def recordIns(self, name, methodName: str, config: MutableMapping[str,
                                                                      Any]):
        '''记录instance传入ins.data'''
        ins = self.instances[self._getTimenow()][name]
        from config.register import RECORDER_LIST
        method = RECORDER_LIST[methodName]
        method({
            "config": config,
            "data": ins.data,
            "tempEnv": {
                "insName": name,
                "ifModule": True,
                "linkDes": str(envGlobal.linkNowNum)
            }
        })
