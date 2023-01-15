from core.typing.fieldType import TYPE_Field, TYPE_Instance

from core.base.file import FileBase

'''
files:
    sumoNet:路网文件
'''

class SumoNetField(FileBase, TYPE_Instance):
    '''sumoField:存放路网文件'''

    def __init__(self):
        super().__init__("tempFile")
        self.init()
