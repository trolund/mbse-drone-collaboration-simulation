import os
from typing import List

import pygame
from dependency_injector.wiring import Provide
from pygame import Vector2
from pygame.rect import Rect

from Models.basic_types import Pos
from Models.env import Env
from Models.drawable import Drawable
from Models.task import Task
from Utils.Utils import map_range
from containers import Container


class Truck(Drawable):
    packages: List[Task] = []
    curr_task = None
    speed = 50  # 0.0 - 1.0

    def __init__(self, grid_pos,
                 size,
                 task_manager,
                 stop_points,
                 packages=None,
                 number_of_attachment_points=1, path=None,
                 env: Env = Provide[Container.env],
                 config=Provide[Container.config]):
        super().__init__()

        self.speed = int(config["setup"]["truck_speed"])

        self.env = env
        self.config = config
        self.task_manager = task_manager
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

    def add_route(self, path, stop_points):
        self.moves = path
        self.stop_points = stop_points

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

    def move(self, ax, ay, bx, by, dt):
        b = Vector2(bx, by)
        b_mag = b.magnitude()

        a = Vector2(ax, ay)

        if b_mag < 20:
            m = map_range(b_mag, 0, 100, 0, self.speed)
            a = a.move_towards(b, m * dt)
        else:
            a = a.move_towards(b, self.speed * dt)

        self.rect.x = a.x
        self.rect.y = a.y

        self.env.home = (self.rect.x + self.size / 2, self.rect.y + self.size / 2)

    def on_tick(self, delta):
        # take new task
        if len(self.moves) > 0 and self.curr_task is None:
            self.curr_task = self.moves.pop(0)

        # Stop the truck if at the stopping position 
        # Stay until all clustered packages are delivered/picked up from the truck
        all_delivered = True

        if self.stop_points != None:
            # print("self.stop_points: ", self.stop_points)
            # print("self.curr_task: ", self.curr_task)
            # print(self.speed)
            # print("left pack to deliver: ", self.task_manager.get_addr_of_tasks_left())
            # print("current cluster: ", self.task_manager.get_curr_cluster())

            if self.curr_task in self.stop_points:
                # print("INNNN")
                self.speed = 0

                addr = self.task_manager.get_addr_of_tasks_left()
                curr_clust = self.task_manager.get_curr_cluster()

                # print("addr: ", addr)
                # print("curr_clust: ", curr_clust)

                for i in curr_clust:
                    if i in addr:
                        all_delivered = False
                
                if all_delivered:
                    # print("ALL delivered")
                    self.speed = int(self.config["setup"]["truck_speed"])

                    self.task_manager.update_curr_cluster()
                    self.stop_points.pop(0)

        # process task when the truck is allowed to move
        if self.curr_task is not None and all_delivered:
            ay = self.rect.y
            ax = self.rect.x
            bx = self.curr_task[0]
            by = self.curr_task[1]

            self.move(ax, ay, bx, by, delta)

            if ax == bx and ay == by:
                self.curr_task = None

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

            self.move(ax, ay, bx, by, delta)

            if ax == bx and ay == by:
                self.curr_task = None

    def get_pos(self):
        return self.grid_pos

    def get_stop_points(self):
        return self.stop_points
