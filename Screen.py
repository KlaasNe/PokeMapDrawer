import os

import Map
import Settings
from Colors import *
from Functions import *
from random import randint


class Screen:
    # w = screen width, h = screen height, df_bg = default background colour
    def __init__(self, df_bg):
        self.df_bg = df_bg
        self.w = Settings.SCREEN_WIDTH
        self.h = Settings.SCREEN_HEIGHT
        self.fs = Settings.FULLSCREEN
        self.surface = pygame.display.set_mode((self.w, self.h), pygame.FULLSCREEN)
        self.map = Map.Map(40, 30)
        pygame.display.init()
        pygame.display.set_caption("PokeMapDrawer")
        pygame.display.set_icon(pygame.image.load(os.path.join("img", "ico.png")))

    def draw_grid(self, x_pos, y_pos, x_size, y_size, x_off, y_off, tiles_x, tiles_y):
        pygame.Surface.fill(self.surface, (0, 0, 0))

        for y in range(0, min(y_size, tiles_y) + 1):
            draw_y = y_pos + y * 16 + y_off
            if y_pos <= draw_y <= y_pos + y_size * 16:
                x1 = max(x_pos + x_off, x_pos)
                x2 = min(x_pos + x_off + tiles_x * 16, x_pos + x_size * 16)
                self.draw_hline(draw_y, x1, x2, GRAY1)

        for x in range(0, min(x_size, tiles_x) + 1):
            draw_x = x_pos + x * 16 + x_off
            if x_pos <= draw_x <= x_pos + x_size * 16:
                y1 = max(y_pos + y_off, y_pos)
                y2 = min(y_pos + y_off + tiles_y * 16, y_pos + y_size * 16)
                self.draw_vline(draw_x, y1, y2, GRAY1)

        pygame.draw.rect(self.surface, GRAY2, (x_pos, y_pos, x_size * 16, y_size * 16), 2)

    def draw_hline(self, y, x1, x2, color):
        pygame.draw.line(self.surface, color, (x1, y), (x2, y))

    def draw_vline(self, x, y1, y2, color):
        pygame.draw.line(self.surface, color, (x, y1), (x, y2))

    def draw_cursor(self, x_off, y_off, color, brush=1):
        mx, my = pygame.mouse.get_pos()
        b_cor = (brush - 1) % 2 * 8 + ((brush - 1) // 2) * 16
        x = ((mx + 3 - x_off % 16 - b_cor) // 16 * 16) - 3 + x_off % 16
        y = ((my + 3 - y_off % 16 - b_cor) // 16 * 16) - 3 + y_off % 16
        pygame.draw.rect(self.surface, color, (x, y, 16 * brush, 16 * brush), 1)

    def change_tile_height(self, x_pos, y_pos, x_off, y_off, brush, lift):
        mx, my = pygame.mouse.get_pos()
        b_cor = (brush - 1) % 2 * 8 + ((brush - 1) // 2) * 16
        x = ((mx + 3 - x_off % 16 - b_cor) // 16 * 16) - 3 + x_off % 16
        y = ((my + 3 - y_off % 16 - b_cor) // 16 * 16) - 3 + y_off % 16
        for y_tile in range(brush):
            for x_tile in range(brush):
                try:
                    self.map.tile_height_info[(y - y_off - y_pos) // 16 + y_tile][(x - x_off - x_pos) // 16 + x_tile] += lift
                except IndexError:
                    pass

    def draw_height_map(self, x_pos, y_pos, x_size, y_size, x_off, y_off):
        heights = pygame.image.load(os.path.join("img", "heights.png"))
        for y in range(self.map.size_y):
            blit_y = y_pos + y_off + 1 + 16 * y
            if blit_y > y_pos + y_size * 16:
                break
            if blit_y + 16 > y_pos:
                for x in range(self.map.size_x):
                    blit_x = x_pos + x_off + 1 + 16 * x
                    if blit_x > x_pos + x_size * 16:
                        break
                    if blit_x + 16 > x_pos:
                        height = self.map.tile_height_info[y][x]
                        if height < 0:
                            self.map.tile_height_info[y][x] = 0
                        if height > 9:
                            self.map.tile_height_info[y][x] = 9
                        self.surface.blit(heights, (blit_x, blit_y), (16 * height, 0, 16, 16))

    def draw_mountains(self, x_pos, y_pos, x_size, y_size, x_off, y_off, hill_type):
        def define_hill_edge_texture(x, y):

            # Looks for the tile heights around (x, y) and adds their relative height to an array. 1 means the tile is
            # situated higher than the central tile, 0 means equal height, -1 means lower
            def get_hills_around_tile():
                current_tile_height = self.map.tile_height_info[y][x]
                hills_around_tile = []
                for around in range(0, 9):
                    try:
                        curr_height = self.map.tile_height_info[y + around // 3 - 1][x + around % 3 - 1]
                        if curr_height > current_tile_height:
                            hills_around_tile.append(1)
                        elif curr_height < current_tile_height:
                            hills_around_tile.append(-1)
                        elif curr_height == current_tile_height:
                            hills_around_tile.append(0)
                    except IndexError:
                        hills_around_tile.append(0)
                return hills_around_tile

            # using the array of relative heights, this calculates the sprite for the hill texture
            hills_around = get_hills_around_tile()
            if self.map.tile_height_info[y][x] < 2: return -1
            elif hills_around[3] == 0 and hills_around[6] == -1 and hills_around[7] == 0:
                return 0 + (5 * hill_type), 1
            elif hills_around[5] == 0 and hills_around[7] == 0 and hills_around[8] == -1:
                return 0 + (5 * hill_type), 2
            elif hills_around[0] == -1 and hills_around[1] == 0 and hills_around[3] == 0:
                return 3 + (5 * hill_type), 0
            elif hills_around[1] == 0 and hills_around[2] == -1 and hills_around[5] == 0:
                return 3 + (5 * hill_type), 0
            elif hills_around[1] == 0 and hills_around[3] == 0 and hills_around[5] == 0 and hills_around[7] == 0:
                return -1
            elif hills_around[1] == 0 and hills_around[3] == -1 and hills_around[7] == 0:
                return 1 + (5 * hill_type), 0
            elif hills_around[3] == 0 and hills_around[5] == 0 and hills_around[7] == -1:
                return 4 + (5 * hill_type), 0
            elif hills_around[1] == 0 and hills_around[5] == -1 and hills_around[7] == 0:
                return 2 + (5 * hill_type), 0
            elif hills_around[1] == -1 and hills_around[3] == 0 and hills_around[5] == 0:
                return 3 + (5 * hill_type), 0
            elif hills_around[1] == -1 and hills_around[3] == -1:
                return 1 + (5 * hill_type), 1
            elif hills_around[3] == -1 and hills_around[7] == -1:
                return 3 + (5 * hill_type), 1
            elif hills_around[5] == -1 and hills_around[7] == -1:
                return 4 + (5 * hill_type), 1
            elif hills_around[1] == -1 and hills_around[5] == -1:
                return 2 + (5 * hill_type), 1
            return -1

        hills = pygame.image.load(os.path.join("img", "hills.png"))
        plants = pygame.image.load(os.path.join("img", "nature.png"))
        for y in range(self.map.size_y):
            blit_y = y_pos + y_off + 1 + 16 * y
            if blit_y > y_pos + y_size * 16:
                break
            if blit_y + 16 > y_pos:
                for x in range(self.map.size_x):
                    blit_x = x_pos + x_off + 1 + 16 * x
                    if blit_x > x_pos + x_size * 16:
                        break
                    if blit_x + 16 > x_pos:
                        height = self.map.tile_height_info[y][x]
                        if height < 0:
                            self.map.tile_height_info[y][x] = 0
                        if height > 9:
                            self.map.tile_height_info[y][x] = 9
                        tile_coo = define_hill_edge_texture(x, y)
                        if tile_coo != -1:
                            tile_x, tile_y = tile_coo
                            self.surface.blit(hills, (blit_x, blit_y), (tile_x * 16, tile_y * 16, 16, 16))
                        else:
                            self.surface.blit(plants, (blit_x, blit_y), (0, 96, 16, 16))

    def draw_black_border(self, pos_x, pos_y, size_x, size_y):
        pygame.draw.rect(self.surface, BLACK, (pos_x - 9, pos_y - 9, size_x * 16 + 19, size_y * 16 + 19), 16)


def main():
    window = Screen(BLACK)
    running = True
    dragging = False
    brush_size = 2
    draw_window_x = 60
    draw_window_y = 60
    mode = "drag"
    vis = "m"
    x_offset, y_offset = 0, 0
    m_start_x, m_start_y = 0, 0
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == ESC:
                    running = False
                    break
                if event.key == key("r"):
                    x_offset = 0
                    y_offset = 0
                if event.key == key("d"):
                    mode = "drag"
                if event.key == key("p"):
                    mode = "paint"
                if event.key == key("m"):
                    vis = "m"
                if event.key == key("h"):
                    vis = "heights"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not dragging and mode == "drag":
                    dragging = True
                    m_start_x, m_start_y = pygame.mouse.get_pos()
                if mode == "paint":
                    if event.button == 1:
                        window.change_tile_height(draw_window_x, draw_window_y, x_offset, y_offset, brush_size, 1)
                    if event.button == 3:
                        window.change_tile_height(draw_window_x, draw_window_y, x_offset, y_offset, brush_size, -1)
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    end_x, end_y = pygame.mouse.get_pos()
                    x_off_delta, y_off_delta = end_x - m_start_x, end_y - m_start_y
                    x_offset += x_off_delta
                    y_offset += y_off_delta
                    m_start_x, m_start_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode == "paint":
                    if event.button == 4:
                        brush_size += 1
                    elif event.button == 5:
                        brush_size -= 1
                    if brush_size <= 0:
                        brush_size = 1

        window.draw_grid(draw_window_x, draw_window_y, 80, 60, x_offset, y_offset, window.map.size_x, window.map.size_y)
        if vis == "m":
            window.draw_mountains(draw_window_x, draw_window_y, 80, 60, x_offset, y_offset, 0)
        elif vis == "heights":
            window.draw_height_map(draw_window_x, draw_window_y, 80, 60, x_offset, y_offset)
        if mode == "paint":
            window.draw_cursor(x_offset, y_offset, RED, brush_size)
        window.draw_black_border(draw_window_x, draw_window_y, 80, 60)
        pygame.display.flip()


if __name__ == '__main__':
    main()
