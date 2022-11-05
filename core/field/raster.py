class Raster:

    def __init__(self, name, row, col, cellSize, nullData=-9999):
        self.name = name
        self.row = row
        self.col = col
        self.cellSize = cellSize
        self.nullData = nullData

        self.data = []

    def define(self, data):
        self.data = data
