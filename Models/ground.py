import pygame
from pygame.surface import Surface

from Models.basic_types import Pos


class Ground:

    def __init__(self, ground, pos: Pos = None, landing_spot: Pos = None):
        self.pos = pos
        self.ground = ground
        self.landing_spot = (10, 10) if landing_spot is None else landing_spot

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

    def get_landing_spot_pos(self, offset=False):
        size = 25
        x_offset = self.landing_spot_width / 2 - size if offset else 0
        y_offset = self.landing_spot_height / 2 - size if offset else 0

        if self.pos is not None:
            return self.landing_spot[0] + self.pos[0] + x_offset, self.landing_spot[1] + self.pos[1] + y_offset
        else:
            return self.landing_spot[0] + x_offset, self.landing_spot[1] + y_offset

    def drew_landing_spot(self, screen):
        (x, y) = self.get_landing_spot_pos()
        pygame.draw.rect(screen, (180, 222, 100), pygame.Rect(x, y, self.landing_spot_width, self.landing_spot_height))