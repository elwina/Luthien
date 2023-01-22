import getopt as getopt
import sys
from core.main import start
from web.web import serverRun


def runDefault():
    start()


arguLen = len(sys.argv)
if arguLen == 1:
    runDefault()
else:
    command=sys.argv[1]
    
    match command:
        case "run":
            start()
        case "web":
            serverRun()
        
                    
