from core.typing.ioType import TYPE_IO_LIST
from core.typing.moduleType import TYPE_MODULE_LIST
from core.typing.fieldType import TYPE_FIELD_LIST
from core.typing.recordType import TYPE_RECORDER_LIST

from core.io.rasterIO import rasterIO
from core.io.raster2IO import raster2IO
from core.io.jsonIO import jsonIO
from core.io.fileListIO import fileListIO
from core.io.geojsonVectorIO import geojsonVectorIO
from core.io.fileMergeIO import fileMergeIO

from module.sumo.io.sumoNet2RoadIO import sumoNet2RoadIO

IO_LIST: TYPE_IO_LIST = {
    "json": jsonIO,
    "txt2Raster": rasterIO,
    "raster": raster2IO,
    "fileList": fileListIO,
    "fileMerge": fileMergeIO,
    "geojson2Vector": geojsonVectorIO,
    "sumoNet2Road": sumoNet2RoadIO,
}

from core.recorder.raster2Recorder import rasterRecorder

# from core.recorder.raster2Recorder import rasterRecorder
from core.recorder.fileRecoder import fileRecorder
from core.recorder.jsonRecoder import jsonRecorder
from core.recorder.vectorRecorder import vectorRecorder

RECORDER_LIST: TYPE_RECORDER_LIST = {
    "raster": rasterRecorder,
    "file": fileRecorder,
    "json": jsonRecorder,
    "vector": vectorRecorder,
}

from module.lisflood.main import Module as lisflood
from module.landslideEva.main import Module as landslideEva
from module.sumo.main import Module as sumo
from module.sumoSpeed.main import Module as sumoSpeed
from module.swmm.main import Module as swmm
from module.geneRain.main import Module as geneRain

MODULE_LIST: TYPE_MODULE_LIST = {
    "lisflood": lisflood,
    "landslideEva": landslideEva,
    "sumo": sumo,
    "sumoSpeed": sumoSpeed,
    "swmm": swmm,
    "geneRain": geneRain,
}

from core.base.listConf import ListConfBase
from core.base.raster2 import RasterBase
from core.base.vector import VectorBase
from core.base.file import FileBase

BASE_LIST = {
    "listConf": ListConfBase,
    "raster": RasterBase,
    "vector": VectorBase,
    "file": FileBase,
}

from core.field.demField import DemField
from core.field.waterField import WaterField
from core.field.tempFileField import TempFileField
from core.field.roadField import RoadField

from module.lisflood.field.uniField import UniField as LisfloodUniField
from module.sumo.field.uniField import UniField as SumoUniField
from module.sumo.field.sumoNetField import SumoNetField
from module.sumoSpeed.field.uniField import UniField as SumoSpeedUniField
from module.swmm.field.uniField import UniField as SwmmUniField
from module.swmm.field.drainPointField import DrainPointField
from module.geneRain.field.uniField import UniField as GeneRainUniField

FIELD_LIST: TYPE_FIELD_LIST = {
    "dem": DemField,
    "rain": WaterField,
    "road": RoadField,
    "tempFile": TempFileField,
    "lisfloodUni": LisfloodUniField,
    "sumoUni": SumoUniField,
    "sumoNet": SumoNetField,
    "sumoSpeedUni": SumoSpeedUniField,
    "swmmUni": SwmmUniField,
    "drainPoint": DrainPointField,
    "geneRainUni": GeneRainUniField,
}
