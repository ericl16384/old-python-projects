import pygame
from pygame.locals import *

def setIcon(iconname):
    icon = pygame.Surface((32,32))
    icon.set_colorkey((255, 255, 255)) #This color is transparent
    rawicon=pygame.image.load(iconname) #Must be 32 x 32
    for i in range(0,32):
        for j in range(0,32):
            icon.set_at((i, j), rawicon.get_at((i, j)))
    pygame.display.set_icon(icon) #Icon set
