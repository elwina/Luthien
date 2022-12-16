from core.typing.moduleType import TYPE_MODULE_LIST
from core.typing.fieldType import TYPE_FIELD_LIST

from module.sample.main import Module as sample

MODULE_LIST: TYPE_MODULE_LIST = {"sample": sample}

from core.base.listConf import ListConfBase
from core.base.raster import RasterBase

BASE_LIST = {"listConf": ListConfBase, "raster": RasterBase}

from core.field.demField import DemField
from module.sample.field.uniField import UniField as SampleUniField

FIELD_LIST: TYPE_FIELD_LIST = {"dem": DemField, "sampleUni": SampleUniField}
