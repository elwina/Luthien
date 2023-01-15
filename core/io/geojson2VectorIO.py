from typing import MutableSequence
from core.typing.ioType import TYPE_IO_Data
'''
config
    outVectorBase: bool

    inFile: bool
    inFilePath: str
    inGeoType: str
'''


def geojson2VectorIO(ioData: TYPE_IO_Data) -> TYPE_IO_Data:
    from core.base.vector import VectorBase
    config = ioData["config"]
    intype = config["inGeoType"]
    ins: VectorBase = ioData["ins"]

    from core.base.vector import VectorData
    data = VectorData()

    if "inFile" in config and config["inFile"] == True:
        filepath = config["inFilePath"]
        from osgeo import ogr
        driver = ogr.GetDriverByName('GeoJSON')
        dataSource = driver.Open(filepath, 0)
        layer = dataSource.GetLayer()

        from core.base.vector import AVector
        objects: MutableSequence[AVector] = []

        if intype == "MultiLineString":
            featNum = layer.GetFeatureCount()
            for i in range(featNum):
                adata = AVector()
                adata.properties = {}
                adata.coordinates = []

                feat = layer.GetFeature(i)
                geom = feat.GetGeometryRef()
                type = geom.GetGeometryName()
                if type != 'MULTILINESTRING':
                    continue
                stringNum = geom.GetGeometryCount()

                propNum = feat.GetFieldCount()
                for j in range(propNum):
                    adata.properties[feat.GetFieldDefnRef(
                        j).GetName()] = feat.GetField(j)

                for j in range(stringNum):
                    geomString = geom.GetGeometryRef(j)
                    stringPoints = geomString.GetPoints()
                    adata.coordinates.append(stringPoints)

                objects.append(adata)

            layer.ResetReading()

            from core.base.vector import VectorData
            data = VectorData()
            data.type = "MultiLineString"
            data.objects = objects

    if "outVectorBase" in config and config["outVectorBase"] == True:
        ins.data = data
        ioData["newData"] = data
    return ioData
