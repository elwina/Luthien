from core.tools.raster2Txt import raster2Txt
from core.typing.recordType import TYPE_A_Record, TYPE_Recorder_Data


def rasterRecorder(rec: TYPE_Recorder_Data) -> None:
    rdata = rec['data']
    env = rec['env']
    filename = env["pre"] + ".ascii"
    raster2Txt(rdata, filename)
