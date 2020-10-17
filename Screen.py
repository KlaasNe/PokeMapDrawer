import pygame
import Settings
import os

from Colors import *


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

    def draw_grid(self, x_pos, y_pos, x_size, y_size, x_off, y_off):
        pygame.Surface.fill(self.surface, (0, 0, 0))

        lx_off, ly_off = x_off % 16, y_off % 16

        for y in range(0, y_size):
            pygame.draw.line(self.surface, GRAY1, (x_pos, y_pos + y * 16 + ly_off), (x_pos + x_size * 16, y_pos + y * 16 + ly_off))

        for x in range(0, x_size):
            pygame.draw.line(self.surface, GRAY1, (x_pos + x * 16 + lx_off, y_pos), (x_pos + x * 16 + lx_off, y_pos + y_size * 16))

        pygame.draw.rect(self.surface, GRAY2, (x_pos, y_pos, x_size * 16, y_size * 16), 2)


def main():
    window = Screen("#000000")
    running = True
    dragging = False
    x_offset, y_offset = 0, 0
    m_start_x, m_start_y = 0, 0
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not dragging:
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

        window.draw_grid(60, 60, 80, 60, x_offset, y_offset)
        pygame.display.flip()


if __name__ == '__main__':
    main()
