from core.base.listConf import ListConfBase
from core.template.inputTemplate import InputTemplate


class UniInput(InputTemplate):

    def __init__(self):
        super(UniInput, self).__init__("uniInput", UniInputField)

    # 返回数据实例
    def get(self):
        return self.instance


if __name__ == "__main__":

    pass
