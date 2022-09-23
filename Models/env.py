import pygame

from Models.ground import Ground
from Models.setup import WIDTH, HEIGHT
from Models.truck import Truck


class Env:
    drones = pygame.sprite.Group()
    tasks = pygame.sprite.Group()
    grounds: list[Ground] = []
    home = ((WIDTH / 2) - 30, (HEIGHT / 2) - 30)
    trucks = pygame.sprite.Group()
