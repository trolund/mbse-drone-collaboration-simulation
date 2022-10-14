import os
from typing import List

import pygame

from Models.package import Package


class Task(pygame.sprite.Sprite):

    packages: List[Package] = []
    number_of_attachment_points: int
    size: int = 50

    def __init__(self, packages=None, number_of_attachment_points=1):
        super().__init__()
        self.packages = packages
        self.number_of_attachment_points = number_of_attachment_points

        self.images = []

        img = pygame.image.load(os.path.join('Assets', 'task.png')).convert_alpha()
        img = pygame.transform.scale(img, (self.size, self.size))

        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def get_lift_requirement(self):
        return sum(p.weight for p in self.packages)
