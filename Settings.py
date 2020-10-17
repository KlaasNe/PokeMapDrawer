from win32api import GetSystemMetrics


SCREEN_WIDTH = GetSystemMetrics(0)
SCREEN_HEIGHT = GetSystemMetrics(1)
FULLSCREEN = True
