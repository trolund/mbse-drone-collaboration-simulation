import pygame

from Models.ground import Ground
from Models.setup import WIDTH, HEIGHT
from Models.task import Task
from Models.truck import Truck


class Env:
    home = ((WIDTH / 2) - 30, (HEIGHT / 2) - 30)
    sprites = pygame.sprite.Group()
    task_ref: list[Task] = []

    # def get_task_at(self, x, y):
    #     return next((t for t in self.tasks if t.rect.x == x and t.rect.y == y), None)