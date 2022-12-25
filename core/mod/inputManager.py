from typing import Literal, MutableMapping, Optional, TypedDict
from core.typing.fieldType import TYPE_Instance
from core.typing.inputType import TYPE_Indata, TYPE_Information

from loguru import logger

'''
TYPE_Information形如
"abc":{
    "required":True
}
'''

'''
TYPE_Indata形如
indata:{
    "dem":{
        #* indata declare
        "method":"in"
        "instance":
    }
}
'''

class inputManager:
    information:TYPE_Information={}
    instances: MutableMapping[str, TYPE_Instance]={}

    def __init__(self):
        pass

    def init(self, inf: TYPE_Information):
        '''确定要输入哪些instance以及其是否必须'''
        self.information=inf

    def receiveData(self,indata:TYPE_Indata):
        '''传入数据函数'''
        newInstances :MutableMapping[str, TYPE_Instance]={}
        for name in indata:
            match indata[name]["method"]:
                case "in":
                    # 处理indata declare
                    if "instance" in indata[name]:
                        ins=indata[name]["instance"]
                        newInstances[name]=ins
                    else:
                        logger.error("No instance input for {name}!",name=name)

        self.instances=newInstances

        # Required Instances检验
        nNames=list(newInstances.keys())
        lackInstances=list(set(self.requiredInstancesName())-(set(nNames)))
        if lackInstances.__len__()>0:
            logger.error("No enough required instances:{lack}",lack=",".join(lackInstances))
        

    def requiredInstancesName(self):
        '''返回required instances名字的列表'''
        return list(map(lambda x:x,filter(lambda x:self.information[x]["required"]==True,self.information)))

    def existOptionalInstancesName(self):
        '''返回存在optional instances名字的列表'''
        return list(set(list(self.instances.keys())) & set(list(map(lambda x:x,filter(lambda x:self.information[x]["required"]==False,self.information)))))

    def getInstances(self):
        '''返回所有instances'''
        return self.instances

