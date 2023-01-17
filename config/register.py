from core.typing.ioType import TYPE_IO_LIST
from core.typing.moduleType import TYPE_MODULE_LIST
from core.typing.fieldType import TYPE_FIELD_LIST
from core.typing.recordType import TYPE_RECORDER_LIST

from core.io.txt2RasterIO import txt2RasterIO
from core.io.jsonIO import jsonIO
from core.io.fileListIO import fileListIO
from core.io.geojson2VectorIO import geojson2VectorIO

from module.sumo.io.sumoNet2RoadIO import sumoNet2RoadIO

IO_LIST: TYPE_IO_LIST = {
    "json": jsonIO,
    "txt2Raster": txt2RasterIO,
    "fileList": fileListIO,
    "geojson2Vector": geojson2VectorIO,
    "sumoNet2Road": sumoNet2RoadIO
}

from core.recorder.rasterRecorder import rasterRecorder
from core.recorder.fileRecoder import fileRecorder
from core.recorder.jsonRecoder import jsonRecorder

RECORDER_LIST: TYPE_RECORDER_LIST = {
    "raster": rasterRecorder,
    "file": fileRecorder,
    "json": jsonRecorder
}

from module.lisflood.main import Module as lisflood
from module.landslideEva.main import Module as landslideEva
from module.sumo.main import Module as sumo
from module.sumoSpeed.main import Module as sumoSpeed

MODULE_LIST: TYPE_MODULE_LIST = {
    "lisflood": lisflood,
    "landslideEva": landslideEva,
    "sumo": sumo,
    "sumoSpeed": sumoSpeed
}

from core.base.listConf import ListConfBase
from core.base.raster import RasterBase
from core.base.vector import VectorBase
from core.base.file import FileBase

BASE_LIST = {
    "listConf": ListConfBase,
    "raster": RasterBase,
    "vector": VectorBase,
    "file": FileBase
}

from core.field.demField import DemField
from core.field.waterField import WaterField
from core.field.tempFileField import TempFileField
from core.field.roadField import RoadField

from module.lisflood.field.uniField import UniField as LisfloodUniField
from module.sumo.field.uniField import UniField as SumoUniField
from module.sumo.field.sumoNetField import SumoNetField
from module.sumoSpeed.field.uniField import UniField as SumoSpeedUniField

FIELD_LIST: TYPE_FIELD_LIST = {
    "dem": DemField,
    "rain": WaterField,
    "road": RoadField,
    "tempFile": TempFileField,
    "lisfloodUni": LisfloodUniField,
    "sumoUni": SumoUniField,
    "sumoNet": SumoNetField,
    "sumoSpeedUni": SumoSpeedUniField
}
