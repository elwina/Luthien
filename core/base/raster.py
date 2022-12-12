class RasterBase:

    def __init__(self, typeName):
        self.typeName = typeName
        self.row = 0
        self.col = 0
        self.cellSize = 0
        self.nullData = 0
        self.data = []

    def init(self, row, col, cellSize, nullData=-9999):
        self.row = row
        self.col = col
        self.cellSize = cellSize
        self.nullData = nullData

    def define(self, data):
        self.data = data
