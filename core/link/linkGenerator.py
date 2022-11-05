import json


class LinkGenerator:

    def __init__(self):
        self.link = {}
        self.fromConfig()

    def fromConfig(self):
        with open("config/link.json") as fp:
            self.link = json.load(fp)

    def getLink(self):
        return self.link