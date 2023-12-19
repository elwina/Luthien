import os
import uuid
from osgeo import gdal, ogr, osr, gdalconst


# 需要注意field，all_touch这些option的值必须为字符串
def vector2raster(
    vectorFile,
    rasterFile,
    outputRasterFile,
    vectorFileDriver="GeoJSON",
    rasterFileDriver="GTiff",
    bands=[1],
    burn_values=[1],
    all_touch="False",
):
    # 输入矢量文件
    vectorFile = vectorFile
    # 输出栅格文件
    outputRasterFile = outputRasterFile
    # 栅格模板文件，确定输出栅格的元数据（坐标系等，栅格大小，范围等）
    rasterFile = rasterFile
    # 打开栅格模板文件
    data = gdal.Open(rasterFile, gdalconst.GA_ReadOnly)
    # 确定栅格大小
    x_res = data.RasterXSize
    y_res = data.RasterYSize
    # 打开矢量文件
    vdriver = ogr.GetDriverByName(vectorFileDriver)
    vector = vdriver.Open(vectorFile)
    # 获取矢量图层
    layer = vector.GetLayer()

    # 创建输出的TIFF栅格文件
    odriver = gdal.GetDriverByName("GTiff")
    targetDataset = odriver.Create(outputRasterFile, x_res, y_res, 1, gdal.GDT_Byte)
    # 设置栅格坐标系与投影
    targetDataset.SetGeoTransform(data.GetGeoTransform())
    targetDataset.SetProjection(data.GetProjection())
    # 目标band 1
    band = targetDataset.GetRasterBand(1)
    # 白色背景
    NoData_value = 0
    band.SetNoDataValue(NoData_value)
    band.FlushCache()
    gdal.RasterizeLayer(
        targetDataset,
        bands,
        layer,
        burn_values=burn_values,
        options=["ALL_TOUCHED=" + all_touch],
    )
    targetDataset = None
    data = None
    vdriver = None


if __name__ == "__main__":
    vector2raster(
        "data/testroad.geojson",
        "data/demtest.txt",
        "data/testout.txt",
        burn_values=[1],
        all_touch="True",
    )
