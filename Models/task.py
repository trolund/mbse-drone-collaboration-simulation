import os
from typing import List
import itertools
import pygame

from Models.package import Package
from Models.drawable import Drawable


class Task(Drawable):
    packages: List[Package] = []
    number_of_attachment_points: int
    size: int = 50
    address: list
    width: int
    height: int
    def __init__(self, address, packages=None, number_of_attachment_points=1):
        

        super().__init__()
        self.packages = packages
        self.address = address
        self.number_of_attachment_points = number_of_attachment_points
        self.width = 5
        self.height = 5

        self.images = []

        img = pygame.image.load(os.path.join('Assets', 'task.png')).convert_alpha()
        img = pygame.transform.scale(img, (self.size * 100, self.size * 100))

        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.id = self.rect

    def get_lift_requirement(self):
        return sum(p.weight for p in self.packages)


    def __str__(self):
        return (f"Package with id xx and weight {self.get_lift_requirement()}, should be delivered to ({self.rect.x},{self.rect.y})")
