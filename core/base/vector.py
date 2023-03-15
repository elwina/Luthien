from copy import deepcopy
import json
import math
import os
from osgeo import ogr
import uuid
from pyproj import Transformer,CRS,Proj
from numba import jit

from typing import Any, Generator, Iterator, MutableMapping, MutableSequence, Sequence, Type, cast
from typing_extensions import Self,assert_type
from core.base.base import BaseBase

from core.typing.ioType import TYPE_IO, TYPE_IO_Data
from core.typing.recordType import TYPE_Recorder, TYPE_Recorder_Env, TYPE_Recorder_TempEnv
from core.base.vectorType import TYPE_COO, TYPE_COO_SST, TYPE_COO_ST, TYPE_COO_T, TYPE_VECTOR_TYPE, AVector, VectorData


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
        re = json.dumps(s, ensure_ascii=False)
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

    def getInsByOneProp(self, propname: str, value) -> Self:
        newIns = deepcopy(self)
        newIns.data.objects = list(
            filter(
                lambda aVec: propname in aVec.properties.keys() and aVec.
                properties.get(propname) == value, newIns.data.objects))
        return newIns

    def getAllAProp(self, propname: str, default="UNDEFINED") -> Sequence[str]:
        return list(
            set(
                list(
                    map(lambda aVec: aVec.properties.get(propname, default),
                        self.data.objects))))

    def getObjByOneProp(self, propname: str, value) -> AVector|None:
        for aVec in self.data.objects:
            if propname in aVec.properties.keys() and aVec.properties.get(
                    propname) == value:
                return aVec
        return None
    
    def getObjByOnePropNew(self, propname: str, value) -> AVector|None:
        vecs=list(filter(lambda aV:propname in aV.properties and aV.properties[propname]==value,self.data.objects))
        if vecs.__len__()!=0:
            return vecs[0]        
        return None

    def getDataTyped(self):
        match self.data.type:
            case "Point":
                return TYPE_COO_T
            case "MultiPoint":
                return TYPE_COO_ST
            case "LineString":
                return TYPE_COO_ST
            case "MultiLineString":
                return TYPE_COO_SST
            case "Polygon":
                return TYPE_COO_ST
            case "MultiPolygon":
                return TYPE_COO_SST

    def trans2Proj(self,inproj:int,outproj:int):
        dataType=self.getDataTyped()
        for obj in self.data.objects:
            if dataType==TYPE_COO_SST:
                obj.coordinates=cast(TYPE_COO_SST,obj.coordinates)
                for coos in obj.coordinates:
                    for i,coo in enumerate(coos):
                        coos[i]=self._transOneCoord(coo,inproj,outproj)
            elif dataType==TYPE_COO_ST:
                obj.coordinates=cast(TYPE_COO_ST,obj.coordinates)
                for i,coo in enumerate(obj.coordinates):
                    obj.coordinates[i]=self._transOneCoord(coo,inproj,outproj)
            elif dataType==TYPE_COO_T:
                obj.coordinates=cast(TYPE_COO_T,obj.coordinates)
                obj.coordinates=self._transOneCoord(obj.coordinates,inproj,outproj)

    def _transOneCoord(self,coo:tuple[float, float], inproj:int, outproj:int)->tuple[float, float]:
        transformer = Transformer.from_crs(inproj,outproj,always_xy=True)
        newcoo=transformer.transform(coo[0],coo[1])
        return newcoo


if __name__ == "__main__":
    v = VectorBase("Vector")
    v.init("MultiLineString")
    from core.io.geojsonVectorIO import geojsonVectorIO
    v.define(geojsonVectorIO, {
        "outVectorBase": True,
        "inFile": True,
        "inFilePath": "data\\a.geojson"
    }, {})
