from module.sample.main import Module as sample
from module.sample2.main import Module as sample2

MODULE_LIST = {"sample": sample, "sample2": sample2}

from core.base.raster import RasterBase

BASE_LIST = {"raster": RasterBase}

from core.field.demField import DemField

FIELD_LIST = {"dem": DemField}
