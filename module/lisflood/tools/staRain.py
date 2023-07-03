from core.field.tempFileField import TempFileField


def staRain(rainField: TempFileField, rainPath: str):
    oldFile = rainField.getAFilePath("rain")
    newstr = ["# auto generate from sta\n"]
    with open(oldFile, "r", encoding="utf-8") as fp:
        rls = fp.readlines()
        newstr.append(f"{rls.__len__()}\tseconds\n")
        for i, line in enumerate(rls):
            arr = line.split()
            rain = 0
            if float(arr[6]) > 0: rain = arr[6]
            newstr.append(f"{rain}\t{i*60}\n")
    with open(rainPath, "w", encoding="utf-8") as fp:
        fp.write("".join(newstr))
    return rainPath
