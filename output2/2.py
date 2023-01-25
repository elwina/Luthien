import math
from core.field.demField import DemField
from core.tools.raster2Txt import raster2Txt

ins = DemField()
ins.init()
ins.defineFromAsciiFile("output2/rrr.ascii")

rdata = ins.data.radata

for line in rdata:
    if all(math.isclose(s, 0.0) for s in line):
        for i in range(len(line)):
            line[i] = -9999.0
    else:
        flag = True
        for i in range(len(line)):
            if math.isclose(line[i], 0.0):
                if flag:
                    line[i] = -9999.0
            else:
                flag = False
                break
        flag = True
        for i in reversed(range(len(line))):
            if math.isclose(line[i], 0.0):
                if flag:
                    line[i] = -9999.0
            else:
                flag = False
                break

for y in reversed(range(len(rdata[0]))):
    for x in reversed(range(len(rdata))):
        if math.isclose(rdata[x][y], -9999.0):
            continue
        if math.isclose(rdata[x][y], 0.0):
            rdata[x][y] = -9999.0
        else:
            break

ins.data.radata = rdata
raster2Txt(ins.data, "output2/4.txt")
