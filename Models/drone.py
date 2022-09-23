import os

import pygame
from pygame.rect import Rect

from Models.basic_types import Move, Pos
from Models.move_type import Move_Type
from Models.task import Task


def get_cor(move: Move):
    return move[0][0], move[0][1]


def get_move_type(move: Move):
    return move[1]


def get_move_obj(move: Move):
    return move[2]


class Drone(pygame.sprite.Sprite):
    size = 70
    lift: float = 22.5

    def __init__(self, env, name=""):
        pygame.sprite.Sprite.__init__(self)
        self.env_ref = env
        self.name = name
        self.moves = []
        self.attachment = None
        self.curr_move = None

        self.images = []

        img = pygame.image.load(os.path.join('Assets', 'drone.png')).convert_alpha()
        img = pygame.transform.scale(img, (self.size, self.size))
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def attach(self, task: Task):

        # print((task.rect.x, task.rect.y), (self.rect.x, self.rect.y))

        if task.rect.x != self.rect.x or task.rect.y != self.rect.y:
            raise Exception('can not attach - drone is not centered over a package! 😤📦', self.name,
                            (self.rect.x, self.rect.y))

        self.attachment = task

    def drop(self):

        if self.attachment is None:
            raise Exception('you can not drop a package you dont have!!!! 😤📦', self.name, (self.rect.x, self.rect.y))

        self.attachment = None

    def add_move_point(self, pos: Pos, name: Move_Type = Move_Type.NORMAL, obj: any = None):
        self.moves.append((pos, name, obj))

    def move_package_with_drone(self):

        if self.attachment is not None:
            self.attachment.rect.x = self.rect.x
            self.attachment.rect.y = self.rect.y

    def process_task(self):
        if self.curr_move is not None:
            ay = self.rect.y
            ax = self.rect.x

            point = get_cor(self.curr_move)

            bx = point[0]
            by = point[1]

            self.do_move(ax, ay, bx, by)

    def do_move(self, ax, ay, bx, by):
        steps_number = max(abs(bx - ax), abs(by - ay))

        if steps_number == 0:
            self.rect = Rect(bx, by, self.size, self.size)
        else:
            step_x = float(bx - ax) / steps_number
            step_y = float(by - ay) / steps_number

            self.rect = Rect(ax + step_x, ay + step_y, self.size, self.size)
            self.rotate(ax, ay, ax + step_x, ay + step_y)

        # is we at the distinction?
        if ax == bx and ay == by:
            # print("!", self.rect.x, self.rect.y, self.name)
            move_type = get_move_type(self.curr_move)

            if move_type == Move_Type.PICKUP:
                obj = get_move_obj(self.curr_move)
                self.attach(obj)
            elif move_type == Move_Type.DROP_OFF:
                self.drop()

                if not self.is_in_drop_zone():
                    print(self.name + " did a drop of that was not in a drop zone 🤬.")

            self.curr_move = None

    def take_task(self):
        if len(self.moves) > 0 and self.curr_move is None:
            self.curr_move = self.moves.pop(0)
            # print(self.curr_move[0], self.name)

    def update(self):
        # take new task
        self.take_task()

        # process task
        self.process_task()

        # move package if it is attached
        self.move_package_with_drone()

    # not done (trying to turn the drone in the direction of flying)
    def rotate(self, ax, ay, bx, by):
        v1 = pygame.math.Vector2(ax, ay)
        v2 = pygame.math.Vector2(bx, by)
        angle_v1_v2_degree = v1.angle_to(v2)

        # self.image = pygame.transform.rotate(self.image, angle_v1_v2_degree)

    def is_in_drop_zone(self):
        for g in self.env_ref.grounds:
            if self.in_zone(g):
                return True

        return False

    def in_zone(self, ground):
        dx, dy = self.rect.x, self.rect.y
        (lpx, lpy) = ground.get_landing_spot_pos()
        lpw, lph = ground.landing_spot_width, ground.landing_spot_height

        if (lpx <= dx <= lpx + lpw) and (lpy <= dy <= lpy + lph):
            return True
        else:
            return False