# Calculates where to draw edges of hills
def create_hill_edges(pmap, hill_type=0, update=False):
    # Determines which sprite to use at (x, y)
    def define_hill_edge_texture(x, y):

        # Looks for the tile heights around (x, y) and adds their relative height to an array. 1 means the tile is
        # situated higher than the central tile, 0 means equal height, -1 means lower
        def get_hills_around_tile():
            current_tile_height = pmap.tile_height_info[(x, y)]
            hills_around_tile = []
            for around in range(0, 9):
                curr_height = pmap.tile_height_info[y + around // 3 - 1][x + around % 3 - 1]
                if curr_height > current_tile_height:
                    hills_around_tile.append(1)
                elif curr_height < current_tile_height:
                    hills_around_tile.append(-1)
                elif curr_height == current_tile_height:
                    hills_around_tile.append(0)
            return hills_around_tile

        # using the array of relative heights, this calculates the sprite for the hill texture
        hills_around = get_hills_around_tile()
        if pmap.tile_height_info.get((x, y), 0) < 2: return -1
        if hills_around[3] == 0 and hills_around[6] == -1 and hills_around[7] == 0:
            return "hi", 0 + (5 * hill_type), 1
        if hills_around[5] == 0 and hills_around[7] == 0 and hills_around[8] == -1:
            return "hi", 0 + (5 * hill_type), 2
        if hills_around[0] == -1 and hills_around[1] == 0 and hills_around[3] == 0:
            return "hi", 3 + (5 * hill_type), 0
        if hills_around[1] == 0 and hills_around[2] == -1 and hills_around[5] == 0:
            return "hi", 3 + (5 * hill_type), 0
        if hills_around[1] == 0 and hills_around[3] == 0 and hills_around[5] == 0 and hills_around[7] == 0:
            return -1
        if hills_around[1] == 0 and hills_around[3] == -1 and hills_around[7] == 0:
            return "hi", 1 + (5 * hill_type), 0
        if hills_around[3] == 0 and hills_around[5] == 0 and hills_around[7] == -1:
            return "hi", 4 + (5 * hill_type), 0
        if hills_around[1] == 0 and hills_around[5] == -1 and hills_around[7] == 0:
            return "hi", 2 + (5 * hill_type), 0
        if hills_around[1] == -1 and hills_around[3] == 0 and hills_around[5] == 0:
            return "hi", 3 + (5 * hill_type), 0
        if hills_around[1] == -1 and hills_around[3] == -1:
            return "hi", 1 + (5 * hill_type), 1
        if hills_around[3] == -1 and hills_around[7] == -1:
            return "hi", 3 + (5 * hill_type), 1
        if hills_around[5] == -1 and hills_around[7] == -1:
            return "hi", 4 + (5 * hill_type), 1
        if hills_around[1] == -1 and hills_around[5] == -1:
            return "hi", 2 + (5 * hill_type), 1
        return -1

    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            hill_edge_texture = define_hill_edge_texture(x, y)
            if hill_edge_texture != -1:
                if hill_edge_texture == ("hi", 3, 0) and pmap.tile_height_info.get((x, y), -1) == pmap.highest_path + 1:
                    hill_edge_texture = ("hi", 0, 3)
                elif update and hill_edge_texture[1] in [1, 2, 3] \
                        and pmap.tile_height_info.get((x, y), -1) > pmap.highest_path + 1:
                    hill_edge_texture = ("hi", hill_edge_texture[1], hill_edge_texture[2] + 2)

                if "ro" != pmap.get_tile_type("ground_layer", x, y) or pmap.get_tile("ground_layer", x, y)[1] < 2:
                    if update:
                        pmap.ground_layer[(x, y)] = hill_edge_texture
                    elif (x, y) not in pmap.ground_layer.keys():
                        pmap.ground_layer[(x, y)] = hill_edge_texture
            elif hill_edge_texture == -1 and "hi" == pmap.get_tile_type("ground_layer", x, y):
                pmap.ground_layer.pop((x, y))
