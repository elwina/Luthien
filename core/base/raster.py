class RasterBase:

    def __init__(self, typeName):
        self.typeName = typeName
        self.row = 0
        self.col = 0
        self.cellSize = 0
        self.nullData = 0
        self.data = []

    def init(self):
        self.row = 100
        self.col = 100
        self.cellSize = 100
        self.nullData = -9999
        self.define([[0 for _ in range(100)] for _ in range(100)])

    def define(self, data):
        self.data = data
