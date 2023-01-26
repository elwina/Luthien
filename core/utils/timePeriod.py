from core.envGlobal import envGlobal as eGl

def timeStepSeconds():
    match eGl.timeUnit:
        case "hour":
            return eGl.timestep*3600
        case default:
            return eGl.timestep*3600