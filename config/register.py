from core.typing.ioType import TYPE_IO_LIST
from core.typing.moduleType import TYPE_MODULE_LIST
from core.typing.fieldType import TYPE_FIELD_LIST
from core.typing.recordType import TYPE_RECORDER_LIST

from core.io.txt2RasterIO import txt2RasterIO
from core.io.jsonIO import jsonIO
from core.io.fileListIO import fileListIO

IO_LIST: TYPE_IO_LIST = {"json": jsonIO, "txt2Raster": txt2RasterIO,"fileList":fileListIO}

from core.recorder.rasterRecorder import rasterRecorder

RECORDER_LIST: TYPE_RECORDER_LIST = {"raster": rasterRecorder}

from module.lisflood.main import Module as lisflood
from module.landslideEva.main import Module as landslideEva

MODULE_LIST: TYPE_MODULE_LIST = {
    "lisflood": lisflood,
    "landslideEva": landslideEva
}

from core.base.listConf import ListConfBase
from core.base.raster import RasterBase

BASE_LIST = {"listConf": ListConfBase, "raster": RasterBase}

from core.field.demField import DemField
from core.field.waterField import WaterField
from core.field.tempFileField import TempFileField
from module.lisflood.field.uniField import UniField as LisfloodUniField

FIELD_LIST: TYPE_FIELD_LIST = {
    "dem": DemField,
    "rain": WaterField,
    "tempFile": TempFileField,
    "lisfloodUni": LisfloodUniField
}
