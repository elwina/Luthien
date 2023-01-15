from osgeo import gdal, ogr, osr, gdalconst


# 需要注意field，all_touch这些option的值必须为字符串
def vector2raster(inputfilePath,
                  outputfile,
                  templatefile,
                  bands=[1],
                  burn_values=[0],
                  field="",
                  all_touch="False"):
    # 输入矢量文件
    inputfilePath = inputfilePath
    # 输出栅格文件
    outputfile = outputfile
    # 栅格模板文件，确定输出栅格的元数据（坐标系等，栅格大小，范围等）
    templatefile = templatefile
    # 打开栅格模板文件
    data = gdal.Open(templatefile, gdalconst.GA_ReadOnly)
    # 确定栅格大小
    x_res = data.RasterXSize
    y_res = data.RasterYSize
    # 打开矢量文件
    ogr.GetDriverByName("GeoJSON")
    vector = ogr.Open(inputfilePath)
    # 获取矢量图层
    layer = vector.GetLayer()
    # 查看要素数量
    featureCount = layer.GetFeatureCount()
    # print(featureCount)

    # 创建输出的TIFF栅格文件
    targetDataset = gdal.GetDriverByName('GTiff').Create(
        outputfile, x_res, y_res, 1, gdal.GDT_Byte)
    # 设置栅格坐标系与投影
    targetDataset.SetGeoTransform(data.GetGeoTransform())
    targetDataset.SetProjection(data.GetProjection())
    # 目标band 1
    band = targetDataset.GetRasterBand(1)
    # 白色背景
    #NoData_value = -999
    NoData_value = 255
    band.SetNoDataValue(NoData_value)
    band.FlushCache()
    if field:
        # 调用栅格化函数。RasterizeLayer函数有四个参数，分别有栅格对象，波段，矢量对象，options
        # options可以有多个属性，其中ATTRIBUTE属性将矢量图层的某字段属性值作为转换后的栅格值
        gdal.RasterizeLayer(
            targetDataset,
            bands,
            layer,
            burn_values=burn_values,
            options=["ALL_TOUCHED=" + all_touch, "ATTRIBUTE=" + field])
    else:
        gdal.RasterizeLayer(targetDataset,
                            bands,
                            layer,
                            burn_values=burn_values,
                            options=["ALL_TOUCHED=" + all_touch])


vector2raster("data/testroad.geojson",
              "data/testout.txt",
              "data/demtest.txt",
              burn_values=[1],
              all_touch="True")
# dem = gdal.Open("data/demtest.txt")
# ogr.GetDriverByName("GeoJSON")
# road = ogr.Open("data/testroad.geojson")

# gdal.RasterizeLayer(dem, [1], road, burn_values=[1])

# print(road)