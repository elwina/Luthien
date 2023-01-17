import json
import os
from osgeo import ogr
import uuid

from typing import Any, MutableMapping, MutableSequence
from core.base.base import BaseBase

from core.typing.ioType import TYPE_IO, TYPE_IO_Data
from core.typing.recordType import TYPE_Recorder, TYPE_Recorder_Env, TYPE_Recorder_TempEnv
from core.base.vectorType import TYPE_VECTOR_TYPE, VectorData


class VectorBase(BaseBase):
    data: VectorData

    def __init__(self, typeName: str):
        self.typeName = typeName
        super().__init__()

    def init(self, type: TYPE_VECTOR_TYPE):
        self.data = VectorData()
        self.data.type = type
        self.data.objects = []

    # 接口函数
    def define(self, method: TYPE_IO, config: MutableMapping[str, Any],
               data: Any):
        config["inGeoType"] = self.data.type
        re = method({"config": config, "ins": self, "newData": data})

    def record(self, method: TYPE_Recorder, config: MutableMapping[str, Any],
               tempEnv: TYPE_Recorder_TempEnv):
        method({"config": config, "ins": self, "tempEnv": tempEnv})

    def toGeoJSONString(self) -> str:
        s = {}
        s["type"] = "FeatureCollection"
        s["features"] = []
        for obj in self.data.objects:
            aFeat = {}
            aFeat["type"] = "Feature"
            aFeat["properties"] = obj.properties
            aFeat["geometry"] = {
                "type": self.data.type,
                "coordinates": obj.coordinates
            }
            s["features"].append(aFeat)
        re = json.dumps(s)
        return re

    def getTempFile(self):
        filepath = os.path.join("temp", str(uuid.uuid4()) + ".geojson")
        f = open(filepath, "w")
        f.write(self.toGeoJSONString())
        f.close()
        return filepath

    def getOgrDatasource(self):
        driver = ogr.GetDriverByName('GeoJSON')
        dataSource = driver.Open(self.getTempFile(), 0)
        return dataSource


if __name__ == "__main__":
    v = VectorBase("Vector")
    v.init("MultiLineString")
    from core.io.geojson2VectorIO import geojson2VectorIO
    v.define(geojson2VectorIO, {
        "outVectorBase": True,
        "inFile": True,
        "inFilePath": "data\\a.geojson"
    }, {})
