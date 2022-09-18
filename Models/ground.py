from typing import List

import pygame
from pygame.surface import Surface


class Ground:
    pos = None
    landing_spot = None

    def __init__(self, ground, pos=None, landing_spot=None):
        self.pos = pos
        self.ground = ground
        self.landing_spot = landing_spot

    def draw(self, screen: Surface):
        res = []

        if self.pos is not None:
            (pos_x, pos_y) = self.pos

            for i in range(len(self.ground)):
                (x, y) = self.ground[i]

                res.append((x + pos_x, y + pos_y))

        pygame.draw.polygon(screen, (127, 252, 20), self.ground if self.pos is None else res)

        pos = self.landing_spot if self.landing_spot is not None else (10, 10)
        pygame.draw.rect(screen, (180, 222, 100), pygame.Rect(pos[0] + self.pos[0] if self.pos is None else 0, pos[1] + self.pos[1] if self.pos is None else 0, 120, 120))


