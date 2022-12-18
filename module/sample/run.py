from core.tools.raster2Txt import raster2Txt


def sampleRun(config):
    rasterData = config.data
    raster2Txt(rasterData, "output/test.dem.ascii")
