import os
from typing import List

import pygame
from pygame.rect import Rect

from Models.package import Package
from Models.drawable import Drawable


class Truck(Drawable):
    packages: List[Package] = []
    curr_task = None

    def __init__(self, grid_pos, size, packages=None, number_of_attachment_points=1, path=None):
        super().__init__()

        self.packages = packages
        self.number_of_attachment_points = number_of_attachment_points
        self.grid_pos = grid_pos

        self.images = []

        self.size = size

        self.width = self.size
        self.height = self.size

        img = pygame.image.load(os.path.join('Assets', 'Truck.png')).convert_alpha()
        img = pygame.transform.scale(img, (self.size * 100, self.size * 100))

        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.rect.x = grid_pos[0]
        self.rect.y = grid_pos[1]

        # truck move
        if path is None:
            self.moves = []
        else:
            self.moves = path
        self.curr_move = None

    def on_tick(self, delta):
        pass

    def on_frame(self, delta):
        pass

    def get_home(self):
        return self.rect.x, self.rect.y

    def add_coordinates(self, x, y):
        self.moves.append((x, y))

    def on_tick(self, delta):
        # take new task
        if len(self.moves) > 0 and self.curr_task is None:
            self.curr_task = self.moves.pop(0)

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

            if ax == bx and ay == by:
                self.curr_task = None
