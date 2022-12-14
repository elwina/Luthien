from module.sample.main import Module as sample
from module.sample2.main import Module as sample2

MODULE_LIST = {"sample": sample, "sample2": sample2}

from core.base.listConf import ListConfBase
from core.base.raster import RasterBase

BASE_LIST = {"listConf": ListConfBase, "raster": RasterBase}

from core.field.demField import DemField
from module.sample.field.uniField import UniField as SampleUniField

FIELD_LIST = {"dem": DemField, "sampleUni": SampleUniField}
