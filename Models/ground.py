from typing import List

import pygame
from pygame.surface import Surface


class Ground:

    def __init__(self, ground):
        self.ground = ground

    def draw(self, screen: Surface):
        pygame.draw.polygon(screen, (127, 252, 20), self.ground)

