import os

import pygame
from pygame.rect import Rect

from Models.move_type import Move_Type
from Models.task import Task

Move = ((int, int), str, any)


def get_cor(move: Move):
    return move[0][0], move[0][1]


def get_move_type(move: Move):
    return move[1]


def get_move_obj(move: Move):
    return move[2]


class Drone(pygame.sprite.Sprite):
    size = 70
    moves = []
    curr_move: Move = None
    lift: float = 22.5
    attachment = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        img = pygame.image.load(os.path.join('Assets', 'drone.png')).convert_alpha()
        img = pygame.transform.scale(img, (self.size, self.size))
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def attach(self, task: Task):

        if task.rect.x is not self.rect.x or task.rect.x is not self.rect.y:
            raise Exception('can not attach - drone is not centered over a package! 😤📦')

        self.attachment = task

    def drop(self):

        if self.attachment is None:
            raise Exception('you can not drop a package you dont have!!!! 😤📦')

        self.attachment = None

    def add_move_point(self, x, y, name: Move_Type = Move_Type.NORMAL, obj: any = None):
        self.moves.append(((x, y), name, obj))

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

            steps_number = max(abs(bx - ax), abs(by - ay))

            if steps_number == 0:
                self.rect = Rect(bx, by, self.size, self.size)
            else:
                step_x = float(bx - ax) / steps_number
                step_y = float(by - ay) / steps_number

                self.rect = Rect(ax + step_x, ay + step_y, self.size, self.size)

            # is we at the distinction?
            if ax == bx and ay == by:
                move_type = get_move_type(self.curr_move)

                if move_type == Move_Type.PICKUP:
                    obj = get_move_obj(self.curr_move)
                    self.attach(obj)
                elif move_type == Move_Type.DROP_OFF:
                    self.drop()

                self.curr_move = None

    def take_task(self):
        if len(self.moves) > 0 and self.curr_move is None:
            self.curr_move = self.moves.pop(0)

    def update(self):
        # take new task
        self.take_task()

        # process task
        self.process_task()

        # move package if it is attached
        self.move_package_with_drone()
