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

        self.drew_landing_spot(screen)

    def drew_landing_spot(self, screen):
        if self.pos is not None:
            pygame.draw.rect(screen, (180, 222, 100), pygame.Rect(10 + self.pos[0], 10 + self.pos[1], 120, 120))
        else:
            pygame.draw.rect(screen, (180, 222, 100), pygame.Rect(10, 10, 120, 120))