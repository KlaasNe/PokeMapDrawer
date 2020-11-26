class Map:
    def __init__(self, size_x, size_y, height=3):
        self.size_x, self.size_y = size_x, size_y
        self.tile_height_info = [[height for x in range(size_x)] for y in range(size_y)]
