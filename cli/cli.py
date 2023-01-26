import getopt
import os
import shutil
import sys
import re


def cli():
    try:
        arguLen = len(sys.argv)
        if arguLen < 3:
            raise Exception("Not enough args!")

        cmd=sys.argv[2]
        match cmd:
            case "add_module":
                if arguLen < 4:
                    raise Exception("Not enough args!")
                moduleName=sys.argv[3]
                
                path=os.path.join("module",moduleName)
                # 增加一个模块
                os.makedirs(path)
                paths=[]
                # 增加三个文件
                files=["information","main","run"]
                for file in files:
                    oldPath=f"template/module/{file}.txt"
                    newPath=os.path.join(path,f"{file}.py")
                    shutil.copy(oldPath,newPath)
                    paths.append(newPath)
                field=os.path.join(path,"field")
                os.makedirs(field)
                oldPath="template/module/field/uniField.txt"
                newPath=os.path.join(field,"uniField.py")
                shutil.copy(oldPath,newPath)
                paths.append(newPath)

                for file in paths:
                    f=open(file,'r',encoding='utf-8')
                    alllines=f.readlines()
                    f.close()
                    f=open(file,'w+',encoding='utf-8')
                    for eachline in alllines:
                        a=re.sub(r'\$\$name\$\$',moduleName,eachline)
                        f.writelines(a)
                    f.close()

    except Exception as e:
        print(e)
        print("Exit!")
        sys.exit(2)


    # try:
    #     opts, args = getopt.getopt(sys.argv[2:], "c:", [])
    #     for opt, arg in opts:
    #         pass
    # except getopt.GetoptError:
    #     print("Wrong Command Line!")
    #     print("Exit!")
    #     sys.exit(2)
    # pass