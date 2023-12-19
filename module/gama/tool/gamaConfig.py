"""
{
    total_people

    building_shapefile
    road_shapefile
    trip_csv_file

    buildingID

    saveCarsOnRoadFolder
}
"""


from pathlib import PurePath


def gamaConfig(target: str, options: dict):
    old_str = [
        "$total_people$",
        "$building_shapefile$",
        "$road_shapefile$",
        "$trip_csv_file$",
        "$buildingID$",
        "$saveCarsOnRoadFolder$",
    ]
    new_str = [
        str(options["total_people"]),
        changePosix(options["building_shapefile"]),
        changePosix(options["road_shapefile"]),
        changePosix(options["trip_csv_file"]),
        options["buildingID"],
        changePosix(options["saveCarsOnRoadFolder"]) + "/",
    ]

    with open("module/gama/tool/tem.gaml", "r", encoding="utf-8") as f1, open(
        target, "w", encoding="utf-8"
    ) as f2:
        for line in f1:
            for i in range(len(old_str)):
                line = line.replace(old_str[i], new_str[i])
            f2.write(line)

    return


def changePosix(string: str):
    string = PurePath(string).as_posix()
    return string
