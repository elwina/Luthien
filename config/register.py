from core.typing.ioType import TYPE_IO_LIST
from core.typing.moduleType import TYPE_MODULE_LIST
from core.typing.fieldType import TYPE_FIELD_LIST

from core.io.txt2RasterIO import txt2RasterIO
from core.io.jsonIO import jsonIO

IO_LIST: TYPE_IO_LIST = {"json": jsonIO, "txt2Raster": txt2RasterIO}

from module.sample.main import Module as sample

MODULE_LIST: TYPE_MODULE_LIST = {"sample": sample}

from core.base.listConf import ListConfBase
from core.base.raster import RasterBase

BASE_LIST = {"listConf": ListConfBase, "raster": RasterBase}

from core.field.demField import DemField
from module.sample.field.uniField import UniField as SampleUniField

FIELD_LIST: TYPE_FIELD_LIST = {"dem": DemField, "sampleUni": SampleUniField}
