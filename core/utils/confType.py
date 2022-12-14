'''
    配置项的类型,支持string,float,int
'''

def generateInitValue(type:str):
    match type:
        case "int":
            return 0
        case "float":
            return 0.0
        case "string":
            return ""
        case default:
            return ""


'''
    [
        {
            "name": "string",
            "type": "string"|"int"|"float"
        }
    ]
'''

def generateInitDict(list:list[dict])->dict:
    return dict(zip([item["name"] for item in list],[generateInitValue(item["type"]) for item in list]))