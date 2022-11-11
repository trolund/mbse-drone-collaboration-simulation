import math
import os
from typing import List

import pygame
from dependency_injector.wiring import Provide
from pygame.rect import Rect

from Models.basic_types import Pos
from Models.env import Env
from Models.drawable import Drawable
from Models.task import Task
from containers import Container


class Truck(Drawable):
    packages: List[Task] = []
    curr_task = None
    speed = 0.00005  # 0.0 - 1.0
    stop = False

    def __init__(self, grid_pos, size, packages=None, number_of_attachment_points=1, path=None, stop_points=None, env: Env = Provide[Container.env]):
        super().__init__()

        self.env = env
        self.packages = packages
        self.number_of_attachment_points = number_of_attachment_points
        self.grid_pos = grid_pos
        self.stop_points: list[(Pos, int)] = stop_points

        self.images = []

        self.size = size

        self.width = self.size
        self.height = self.size

        self.velocity = 20

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

    def move_package_with_truck(self):
        for t in self.packages:
            if not t.is_taken():
                x, y = self.get_home()
                t.rect.x = x
                t.rect.y = y

    def on_frame(self, delta):
        pass

    def get_home(self):
        return self.rect.x + (self.size / 2), self.rect.y + (self.size / 2)

    def add_coordinates(self, x, y):
        self.moves.append((x, y))

    def on_tick(self, delta):
        self.env.home = (self.rect.x, self.rect.y)

        # take new task
        self.take_task(delta)

        # process task
        if not self.stop:
            self.process_task()

        # move packages with truck
        self.move_package_with_truck()
        return self.rect.x, self.rect.y

    def take_task(self, delta):
        if len(self.moves) > 0 and self.curr_task is None:
            self.curr_task = self.moves.pop(0)

    def process_task(self):
        if self.curr_task is not None:
            ay = self.rect.y
            ax = self.rect.x

            bx = self.curr_task[0]
            by = self.curr_task[1]

            steps_number = steps_number = max(abs(bx - ax), abs(by - ay))

            if steps_number == 0:
                self.rect = Rect(bx, by, self.size, self.size)
            else:
                stepx = float(bx - ax) / steps_number
                stepy = float(by - ay) / steps_number
                self.rect = Rect(ax + stepx, ay + stepy, self.size, self.size)

            if ax == bx and ay == by:
                self.curr_task = None

    def get_pos(self):
        return self.grid_pos