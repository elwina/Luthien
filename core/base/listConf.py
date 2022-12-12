from typing import Any


class ListConf:

    def __init__(self, name: str, list: list[str]):
        self.name = name
        self.list = list
        self.data: dict[str, Any] = dict(zip(list, [1 for _ in list]))

    def setter(self, key: str, value: str):
        self.data[key] = value


if __name__ == "__main__":
    lc = ListConf("test", ["12,123,432"])
    lc.setter("12", "wer")
