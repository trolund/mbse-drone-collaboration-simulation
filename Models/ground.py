import pygame
from pygame.surface import Surface

from Models.basic import Pos


class Ground:

    def __init__(self, ground, pos: Pos=None, landing_spot: Pos=None):
        self.pos = pos
        self.ground = ground
        self.landing_spot = landing_spot

        self.landing_spot_width = 150
        self.landing_spot_height = 150

    def draw(self, screen: Surface):
        res = []

        if self.pos is not None:
            (pos_x, pos_y) = self.pos

            for i in range(len(self.ground)):
                (x, y) = self.ground[i]

                res.append((x + pos_x, y + pos_y))

        pygame.draw.polygon(screen, (127, 252, 20), self.ground if self.pos is None else res)

        self.drew_landing_spot(screen)

    def drew_landing_spot(self, screen):
        if self.pos is not None:
            pygame.draw.rect(screen, (180, 222, 100), pygame.Rect(10 + self.pos[0], 10 + self.pos[1], self.landing_spot_width, self.landing_spot_height))
        else:
            pygame.draw.rect(screen, (180, 222, 100), pygame.Rect(10, 10, self.landing_spot_width, self.landing_spot_height))