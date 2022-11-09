from core.init import init
from core.link.moduleInf import ModuleInf
from core.main import start

Global = {"BasicConfig": {}, "moduleInformation": {}}

init(Global)

start(Global)