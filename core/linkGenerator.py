import commentjson as json
from config.path import LINK_JSON_PATH
from core.typing.linkType import TYPE_Link_Json


class LinkGenerator:
    link: TYPE_Link_Json

    def __init__(self):
        self.fromConfig()

    def fromConfig(self):
        with open(LINK_JSON_PATH) as fp:
            self.link = json.load(fp)

    def getLink(self):
        return self.link["link"]


if __name__ == "__main__":
    lg = LinkGenerator()
    link = lg.getLink()
    print(link)
