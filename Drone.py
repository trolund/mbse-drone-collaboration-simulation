import os

import pygame
from pygame.rect import Rect


class Drone(pygame.sprite.Sprite):

    size = 50

    tasks = []
    curr_task = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        img = pygame.image.load(os.path.join('Assets', 'drone.png')).convert()
        img = pygame.transform.scale(img, (self.size, self.size))
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def add_coordinates(self, x, y):
        self.tasks.append((x, y))

    def update(self):
        # take new task
        if len(self.tasks) > 0 and self.curr_task is None:
            self.curr_task = self.tasks.pop(0)

        # process task
        if self.curr_task is not None:
            ay = self.rect.y
            ax = self.rect.x

            bx = self.curr_task[0]
            by = self.curr_task[1]

            steps_number = max(abs(bx - ax), abs(by - ay))

            if steps_number == 0:
                self.rect = Rect(bx, by, self.size, self.size)
            else:
                stepx = float(bx - ax) / steps_number
                stepy = float(by - ay) / steps_number
                self.rect = Rect(ax + stepx, ay + stepy, self.size, self.size)

            print(ax, ay, len(self.tasks))

            if ax == bx and ay == by:
                self.curr_task = None




