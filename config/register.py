from core.typing.ioType import TYPE_IO_LIST
from core.typing.moduleType import TYPE_MODULE_LIST
from core.typing.fieldType import TYPE_FIELD_LIST
from core.typing.recordType import TYPE_RECORDER_LIST

from core.io.txt2RasterIO import txt2RasterIO
from core.io.jsonIO import jsonIO

IO_LIST: TYPE_IO_LIST = {"json": jsonIO, "txt2Raster": txt2RasterIO}

from core.recorder.rasterRecoder import rasterRecorder

RECORDER_LIST: TYPE_RECORDER_LIST = {"raster": rasterRecorder}

from module.sample.main import Module as sample
from module.lisflood.main import Module as lisflood

MODULE_LIST: TYPE_MODULE_LIST = {"sample": sample, "lisflood": lisflood}

from core.base.listConf import ListConfBase
from core.base.raster import RasterBase

BASE_LIST = {"listConf": ListConfBase, "raster": RasterBase}

from core.field.demField import DemField
from core.field.rainField import RainField
from module.sample.field.uniField import UniField as SampleUniField
from module.lisflood.field.uniField import UniField as LisfloodUniField

FIELD_LIST: TYPE_FIELD_LIST = {
    "dem": DemField,
    "rain": RainField,
    "sampleUni": SampleUniField,
    "lisfloodUni": LisfloodUniField
}
