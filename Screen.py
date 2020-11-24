import os

import Map
import Settings
from Colors import *
from Functions import *


class Screen:
    # w = screen width, h = screen height, df_bg = default background colour
    def __init__(self, df_bg):
        self.df_bg = df_bg
        self.w = Settings.SCREEN_WIDTH
        self.h = Settings.SCREEN_HEIGHT
        self.fs = Settings.FULLSCREEN
        self.surface = pygame.display.set_mode((self.w, self.h), pygame.FULLSCREEN)
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


def main():
    window = Screen(BLACK)
    world = Map.Map(40, 30)
    running = True
    dragging = False
    brush_size = 2
    mode = "drag"
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not dragging and mode == "drag":
                    dragging = True
                    m_start_x, m_start_y = pygame.mouse.get_pos()
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

        window.draw_grid(60, 60, 80, 60, x_offset, y_offset, 40, 30)
        if mode == "paint":
            window.draw_cursor(x_offset, y_offset, RED, brush_size)
        pygame.display.flip()


if __name__ == '__main__':
    main()
