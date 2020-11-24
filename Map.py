class Map:
    def __init__(self, size_x, size_y, height=0):
        self.size_x, self.size_y = size_x, size_y
        self.tile_height_info = [[height] * size_x] * size_y
