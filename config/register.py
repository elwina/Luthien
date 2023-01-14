from core.typing.ioType import TYPE_IO_LIST
from core.typing.moduleType import TYPE_MODULE_LIST
from core.typing.fieldType import TYPE_FIELD_LIST
from core.typing.recordType import TYPE_RECORDER_LIST

from core.io.txt2RasterIO import txt2RasterIO
from core.io.jsonIO import jsonIO
from core.io.fileListIO import fileListIO

IO_LIST: TYPE_IO_LIST = {
    "json": jsonIO,
    "txt2Raster": txt2RasterIO,
    "fileList": fileListIO
}

from core.recorder.rasterRecorder import rasterRecorder
from core.recorder.fileRecoder import fileRecorder

RECORDER_LIST: TYPE_RECORDER_LIST = {
    "raster": rasterRecorder,
    "file": fileRecorder
}

from module.lisflood.main import Module as lisflood
from module.landslideEva.main import Module as landslideEva
from module.sumo.main import Module as sumo

MODULE_LIST: TYPE_MODULE_LIST = {
    "lisflood": lisflood,
    "landslideEva": landslideEva,
    "sumo": sumo
}

from core.base.listConf import ListConfBase
from core.base.raster import RasterBase

BASE_LIST = {"listConf": ListConfBase, "raster": RasterBase}

from core.field.demField import DemField
from core.field.waterField import WaterField
from core.field.tempFileField import TempFileField
from module.lisflood.field.uniField import UniField as LisfloodUniField
from module.sumo.field.uniField import UniField as SumoUniField

FIELD_LIST: TYPE_FIELD_LIST = {
    "dem": DemField,
    "rain": WaterField,
    "tempFile": TempFileField,
    "lisfloodUni": LisfloodUniField,
    "sumoUni": SumoUniField
}
