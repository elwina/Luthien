from config.basic import MODULE_LIST


class Coupler:

    def __init__(self, coupleData):
        # 找到模块
        self.module = MODULE_LIST[coupleData["module"]]

        # 处理input
        self.input = []

        self.output = []

    def inputProcess(self, inputInf):
        re = {}

        # default value
        re = inputInf["default"]["value"]

        # predefine value
        re = inputInf["preDefine"]["value"]

        # level loop

    def levelLoop(self, levelInf):

        pass
