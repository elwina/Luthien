import json
from typing import MutableSequence
from core.typing.ioType import TYPE_IO_Data

"""
config
    outVectorBase: bool

    inOldData: bool
    inFilePath: str
    inGeoType: str

    outProj:int
    inProj:int
"""


def geojsonVectorIO(ioData: TYPE_IO_Data) -> int:
    from core.base.vector import VectorBase

    config = ioData["config"]
    intype = config["inGeoType"]
    ins: VectorBase = ioData["ins"]

    from core.base.vectorType import VectorData

    data = VectorData()

    if "inOldData" in config and config["inOldData"] == True:
        data = ins.data

    if "inFilePath" in config and config["inFilePath"] != "":
        filepath = config["inFilePath"]

        from core.base.vectorType import AVector

        objects: MutableSequence[AVector] = []

        if intype == "MultiLineString":
            from osgeo import ogr

            driver = ogr.GetDriverByName("GeoJSON")
            dataSource = driver.Open(filepath, 0)
            layer = dataSource.GetLayer()

            featNum = layer.GetFeatureCount()
            for i in range(featNum):
                adata = AVector()
                adata.properties = {}
                adata.coordinates = []

                feat = layer.GetFeature(i)
                geom = feat.GetGeometryRef()
                type = geom.GetGeometryName()
                if type != "MULTILINESTRING":
                    continue
                stringNum = geom.GetGeometryCount()

                propNum = feat.GetFieldCount()
                for j in range(propNum):
                    adata.properties[feat.GetFieldDefnRef(j).GetName()] = feat.GetField(
                        j
                    )

                for j in range(stringNum):
                    geomString = geom.GetGeometryRef(j)
                    stringPoints = geomString.GetPoints()
                    adata.coordinates.append(stringPoints)

                objects.append(adata)

            layer.ResetReading()

            data.type = "MultiLineString"
            data.objects = objects
        if intype == "Polygon":
            data.type = "Polygon"
            with open(filepath, "r", encoding="utf-8") as f:
                geojson = json.load(f)

                fobjects = list(
                    filter(
                        lambda x: x["geometry"]["type"] == "Polygon",
                        geojson["features"],
                    )
                )

                def mapfunc(x):
                    adata = AVector()
                    adata.properties = x["properties"]
                    adata.coordinates = x["geometry"]["coordinates"][0]
                    return adata

                objects = list(
                    map(
                        mapfunc,
                        fobjects,
                    )
                )
            data.objects = objects
        if intype == "Point":
            data.type = "Point"
            with open(filepath, "r", encoding="utf-8") as f:
                geojson = json.load(f)

                fobjects = list(
                    filter(
                        lambda x: x["geometry"]["type"] == "Point",
                        geojson["features"],
                    )
                )

                def mapfunc(x):
                    adata = AVector()
                    adata.properties = x["properties"]
                    adata.coordinates = x["geometry"]["coordinates"]
                    return adata

                objects = list(
                    map(
                        mapfunc,
                        fobjects,
                    )
                )

    ins.data = data
    if "outProj" in config and "inProj" in config:
        ins.trans2Proj(config["inProj"], config["outProj"])
        data = ins.data

    return 0
