import xml.etree.ElementTree as ET
import pandas


def statistic(summaryPath: str, tripinfoPath: str, queuePath: str,
              lanaDataPath: str):
    summary = ET.ElementTree(file=summaryPath).getroot()
    meanSpeed = {"time": [], "meanSpeed": []}
    for child in summary.findall(".//step"):
        meanSpeed["time"].append(child.get("time"))
        meanSpeed["meanSpeed"].append(child.get("meanSpeed"))
    meanSpeedDF = pandas.DataFrame(meanSpeed)
    meanSpeedDF.to_csv("output/lab/meanSpeed50.csv")

    # tripinfo = ET.ElementTree(file=tripinfoPath).getroot()
    # carinfo = {"departTime": [], "duration": []}
    # for child in tripinfo.findall(".//tripinfo"):
    #     carinfo["departTime"].append(child.get("depart"))
    #     carinfo["duration"].append(child.get("duration"))
    # carinfoDF = pandas.DataFrame(carinfo)
    # carinfoDF.to_csv("output/lab/car50.csv")

    # queue = ET.ElementTree(file=queuePath).getroot()
    # queueinfo = {"time": [], "totalQueue": []}
    # for child in queue.findall(".//data"):
    #     lanes = child.find(".//lanes")
    #     if lanes is None: continue
    #     q = 0.0
    #     for lane in lanes.findall(".//lane"):
    #         q = q + float(lane.get("queueing_time"))  # type: ignore
    #     queueinfo["time"].append(child.get("timestep"))
    #     queueinfo["totalQueue"].append(q)
    # queueDF = pandas.DataFrame(queueinfo)
    # queueDF.to_csv("output/lab/queue2.csv")

    # lanedata = ET.ElementTree(file=lanaDataPath).getroot()
    # lanedatainfo = {"laneID": [], "occupancy": []}
    # for child in lanedata.findall(".//lane"):
    #     lanedatainfo["laneID"].append(child.get("id"))
    #     lanedatainfo["occupancy"].append(child.get("occupancy"))
    # lanedataDF = pandas.DataFrame(lanedatainfo)
    # lanedataDF.to_csv("output/lab/lane2.csv")


statistic(
    "output/czs3-50/Out_0013_sumo_files_0_4_1.summary.xml",
    "output/czs3-50/Out_0012_sumo_files_0_4_0.tripinfo.xml",
    "output/czs2/Out_0019_sumo_files_0_5_3.queue.xml",
    "output/czs2/Out_0018_sumo_files_0_5_2.lanedata.xml",
)
