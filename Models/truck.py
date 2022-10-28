import os
from typing import List

import pygame

from Models.package import Package


class Truck(pygame.sprite.Sprite):
    packages: List[Package] = []

    def __init__(self, grid_pos, scale, packages=None, number_of_attachment_points=1):
        super().__init__()
        self.packages = packages
        self.number_of_attachment_points = number_of_attachment_points
        self.grid_pos = grid_pos

        self.images = []

        self.width = 27
        self.height = 11

        img = pygame.image.load(os.path.join('Assets', 'Truck.png')).convert_alpha()
        img = pygame.transform.scale(img, (self.width * 100, self.height * 100))

        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.rect.x = grid_pos[0]
        self.rect.y = grid_pos[1]

    def update(self, scale):
        pass

    def draw(self):
        pass
    def get_home(self):
        return self.rect.x, self.rect.y