from collections import deque

import pygame

from Models.setup import WIDTH, HEIGHT
from Models.task import Task


class Env:
    home = ((WIDTH / 2) - 30, (HEIGHT / 2) - 30)

    # all sprirtes displayed on screen
    sprites = pygame.sprite.Group()

    task_ref = deque()
    truck_ref = None
    # drone_ref: list[Drone] = []

    # def get_task_at(self, x, y):
    #     return next((t for t in self.tasks if t.rect.x == x and t.rect.y == y), None)