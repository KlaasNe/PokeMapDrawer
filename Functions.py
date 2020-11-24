import pygame


# Returns a pygame key
def key(k):
    return getattr(pygame, "K_" + k)


ESC = key("ESCAPE")
