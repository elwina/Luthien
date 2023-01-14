from core.typing.fieldType import TYPE_Field

from core.base.file import FileBase


class TempFileField(FileBase, TYPE_Field):
    '''内置Field:任意文件列表'''

    def __init__(self):
        super().__init__("tempFile")
        self.init()