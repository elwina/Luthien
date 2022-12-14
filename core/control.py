from core.fieldManager import FieldManager
from core.link.linkGenerator import LinkGenerator
from config.register import MODULE_LIST, FIELD_LIST
from loguru import logger


class Control():

    def __init__(self, Global):
        self.timestep = 0
        self.getLink()
        self.Global = Global

        self.initialize()

    def getLink(self):
        lGr = LinkGenerator()
        self.linkSheet = lGr.getLink()

    def initialize(self):
        self.fMr = FieldManager()
        self.fMr.createField(FIELD_LIST)

    def run(self):
        for action in self.linkSheet:
            logger.info("Start Run Module {module_name}",
                        module_name=action["module"])
            self.runOne(action)

    def runOne(self, action):
        mo = MODULE_LIST[action["module"]]
