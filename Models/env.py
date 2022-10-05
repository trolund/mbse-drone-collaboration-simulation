import pygame

from Models.ground import Ground
from Models.setup import WIDTH, HEIGHT
from Models.truck import Truck


class Env:

    grounds: list[Ground] = []
    home = ((WIDTH / 2) - 30, (HEIGHT / 2) - 30)
    trucks = pygame.sprite.Group()

    # ref to objects
    drones_ref = []
    tasks_ref = []

    # object that should be drawn to screen
    drones = pygame.sprite.Group()
    tasks = pygame.sprite.Group()

    def get_task_at(self, x, y):
        return next((t for t in self.tasks if t.rect.x == x and t.rect.y == y), None)