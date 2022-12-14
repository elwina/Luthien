class InputTemplate:

    def __init__(self, name: str, Field):
        self.name = name
        self.field = Field
        self.instance = Field()
