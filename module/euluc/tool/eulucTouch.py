from osgeo import ogr, gdal, gdalconst, osr
from pyproj import Transformer


def eulucTouch(
    vectorFileDriver="ESRI Shapefile",
    eulucFile="D:/Workspace/luthien3/source/EULUC-China-2018/euluc-latlonnw.shp",
):
    vdriver = ogr.GetDriverByName("GeoJSON")
    shapefile = "D:/Workspace/luthien3/newSZ/building.geojson"

    dataSource = vdriver.Open(shapefile, gdalconst.GA_ReadOnly)
    layer = dataSource.GetLayer()

    nds = vdriver.CopyDataSource(dataSource, "D:/Workspace/luthien3/newSZ/new3.geojson")
    nds.Destroy()
    nds = vdriver.Open("D:/Workspace/luthien3/newSZ/new3.geojson", 1)
    layer2 = nds.GetLayer()

    transformer = Transformer.from_crs(4326, 32650, always_xy=True)

    rasterFile = "D:/Workspace/luthien3/newSZ/euluc-tif.tif"
    driver = gdal.GetDriverByName("GTiff")
    raster = gdal.Open(rasterFile, gdalconst.GA_ReadOnly)
    band = raster.GetRasterBand(1)

    layer2.CreateField(ogr.FieldDefn("euluc", ogr.OFTInteger))

    for feature in layer2:
        geom = feature.GetGeometryRef()
        # 获取质心
        cpoint = geom.Centroid()
        # print(geom.GetGeometryName())
        x = cpoint.GetX()
        y = cpoint.GetY()
        x, y = transformer.transform(x, y)

        # 获取行列、波段
        rows = raster.RasterYSize
        cols = raster.RasterXSize
        bands = raster.RasterCount
        # 获取放射变换信息
        transform = raster.GetGeoTransform()
        xOrigin = transform[0]
        yOrigin = transform[3]
        pixelWidth = transform[1]
        pixelHeight = transform[5]
        xOffset = int((x - xOrigin) / pixelWidth)
        yOffset = int((y - yOrigin) / pixelHeight)
        data = band.ReadAsArray(xOffset, yOffset, 1, 1)
        value = data[0, 0]

        valueint = int(value)
        # print(value)

        feature.SetField("euluc", valueint)
        layer2.SetFeature(feature)

        # for basefeature in layer:
        #     basegeom = basefeature.GetGeometryRef()
        #     if basegeom.Contains(cpoint):
        #         print(basefeature.GetField("Level1"))
        #     pass

    nds.Destroy()
    pass


eulucTouch()
