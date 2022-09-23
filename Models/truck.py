import os
from typing import List

import pygame

from Models.package import Package


class Truck(pygame.sprite.Sprite):

    packages: List[Package] = []

    def __init__(self, packages=None, number_of_attachment_points=1):
        super().__init__()
        self.packages = packages
        self.number_of_attachment_points = number_of_attachment_points

        self.images = []

        self.scale = 3
        self.width = 855 / self.scale
        self.height = 352 / self.scale

        img = pygame.image.load(os.path.join('Assets', 'Truck.png')).convert_alpha()
        img = pygame.transform.scale(img, (self.width, self.height))

        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def draw(self):
        pass



