from copy import deepcopy
from typing import Any, MutableMapping, Protocol, Sequence
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

    instances: MutableMapping[str, MutableMapping[int, Any]]
    '''
    instances形如
    {
        out1:{
            atime:instance
        }
    }
    '''

    def __init__(self):
        pass

    def init(self, inf: TYPE_Output_Information):
        self.information = inf
        self.instances = {}
        for name in inf:
            self.instances[name] = {}

    def _getTimenow(self):
        return envGlobal.epoch

    def clearCache(self):
        '''清除缓存的函数,备用'''
        self.instances = dict(
            map(
                lambda x: (x[0],
                           dict(
                               filter(lambda y: y[0] >= self._getTimenow(), x[
                                   1].items()))), self.instances.items()))

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
                self.instances[name][atime] = deepcopy(ins)

    def getOutputData(self, name: str) -> MutableMapping[int, Any]:
        '''获得output ins data'''
        if name in self.instances:
            return dict(
                map(lambda x: (x[0], x[1].data), self.instances[name].items()))
        return {}

    def makeRecords(self, recordList: Sequence[TYPE_Record_Declare]):
        '''记录'''
        for record in recordList:
            self.recordIns(record["catch"], record["method"], record["config"])
        logger.success("Sucessfully make records in outMr.")

    def recordIns(self, name: str, methodName: str,
                  config: MutableMapping[str, Any]):
        '''记录instance传入ins.data'''
        ins = self.instances[name][self._getTimenow()]
        from config.register import RECORDER_LIST
        method = RECORDER_LIST[methodName]
        method({
            "config": config,
            "ins": ins,
            "tempEnv": {
                "insName": name,
                "ifModule": True,
                "linkDes": str(envGlobal.linkNowNum)
            }
        })
