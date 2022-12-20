from typing import Literal, MutableMapping, Optional, TypedDict
from loguru import logger
from core.typing.fieldType import TYPE_Instance
from core.typing.inputType import TYPE_Indata, TYPE_Information

'''
"abc":{
    "required":True
}
'''

'''
indata:{
    "dem":{
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
        '''传入数据重要函数'''
        newInstances :MutableMapping[str, TYPE_Instance]={}
        for name in indata:
            match indata[name]["method"]:
                case "in":
                    ins=indata[name].get("instance")
                    if ins is not None:
                        newInstances[name]=ins
                    else:
                        logger.error("No Instance Input!")

        self.instances=newInstances

        # Required Instances检验
        nNames=list(newInstances.keys())
        lackInstances=list(set(self.requiredInstancesName())-(set(nNames)))
        if lackInstances.__len__()>0:
            logger.error("No Enough Required Instances:{lack}",lack=",".join(lackInstances))
        

    def requiredInstancesName(self):
        '''返回required instances名字的列表'''
        return list(map(lambda x:x,filter(lambda x:self.information[x]["required"]==True,self.information)))

    def existOptionalInstancesName(self):
        '''返回存在optional instances名字的列表'''
        return list(set(list(self.instances.keys())) & set(list(map(lambda x:x,filter(lambda x:self.information[x]["required"]==False,self.information)))))

    def getInstances(self):
        return self.instances

if __name__=="__main__":
    m=inputManager()
    m.init({
        "abc":{
            "required":True
        },
        "abc2":{
            "required":False
        },
    })

    # m.receiveData({
    #     "abc":{
    #        "method":"in",
    #        "instance":"s"
    #     },
    #     "abc2":{
    #        "method":"in",
    #        "instance":"s"
    #     }
    # })