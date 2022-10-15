import os
from typing import List

import pygame

from Models.package import Package


class Truck(pygame.sprite.Sprite):
    packages: List[Package] = []

    def __init__(self, scale, packages=None, number_of_attachment_points=1):
        super().__init__()
        self.packages = packages
        self.number_of_attachment_points = number_of_attachment_points

        self.images = []

        self.width = 27 * scale
        self.height = 11 * scale

        img = pygame.image.load(os.path.join('Assets', 'Truck.png')).convert_alpha()
        img = pygame.transform.scale(img, (self.width, self.height))

        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        (rot_image, rot_rect) = self.rot_center(self.image, self.rect, 90)

        self.image = rot_image
        self.rect = rot_rect

        self.rect.x = 560
        self.rect.y = 800

    def update(self, scale):
        self.width = 27 * scale
        self.height = 11 * scale

    def draw(self):
        pass

    def get_home(self):
        return self.rect.x, self.rect.y

    def rot_center(self, image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect

    def rot_front_wheels(self, image, rect, angle):
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.right)
        return rot_image, rot_rect
