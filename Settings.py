from win32api import GetSystemMetrics


SCREEN_WIDTH = GetSystemMetrics(0)//2
SCREEN_HEIGHT = GetSystemMetrics(1)//2
FULLSCREEN = True
