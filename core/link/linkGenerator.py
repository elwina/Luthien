import commentjson as json
from config.path import LINK_JSON_PATH


class LinkGenerator:

    def __init__(self):
        self.link = {}
        self.fromConfig()

    def fromConfig(self):
        with open(LINK_JSON_PATH) as fp:
            self.link = json.load(fp)["link"]

    def getLink(self):
        return self.link


if __name__ == "__main__":
    lg = LinkGenerator()
    link = lg.getLink()
    print(link)
