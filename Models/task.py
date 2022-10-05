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
        self.attachment_points_used = [False for x in range(number_of_attachment_points)]

        self.images = []

        img = pygame.image.load(os.path.join('Assets', 'task.png')).convert_alpha()
        img = pygame.transform.scale(img, (self.size * number_of_attachment_points, self.size))

        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def get_lift_requirement(self):
        if self.packages is None or len(self.packages) == 0:
            return 0

        return sum(p.wight for p in self.packages)

    def can_lift(self, drone):
        can_lift_whight = drone.lift_capacity > self.get_lift_requirement()
        all_drones_attached = all(x for x in self.attachment_points_used)

        print(can_lift_whight, all_drones_attached, self.attachment_points_used)

        return can_lift_whight and all_drones_attached

    def get_attachment_point(self):
        index = self.attachment_points_used.index(False)
        return index, (self.rect.x + (index * self.size), self.rect.y)

    def confirm_attachment(self, index):
        self.attachment_points_used[index] = True