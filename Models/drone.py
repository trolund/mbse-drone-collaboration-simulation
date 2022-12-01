import os
import uuid

import pygame
from dependency_injector.wiring import Provide
from pygame import Vector2

from Cominication_hub.BaseMediator import BaseMediator
from Logging.eventlogger import EventLogger
from Models.basic_types import Move, Pos
from Models.drone_mode import DroneMode
from Models.env import Env
from Models.move_type import Move_Type
from Models.task import Task
from Utils.Utils import map_range
from Utils.layout_utils import distance_between
from containers import Container
from Models.drawable import Drawable
from Models.Battery import Battery


def get_cor(move: Move):
    return move[0][0], move[0][1]


def get_move_type(move: Move):
    return move[1]


def get_move_obj(move: Move):
    return move[2]


SCALED_IMAGE = None


def get_scaled_image(size):
    global SCALED_IMAGE
    if SCALED_IMAGE is None:
        SCALED_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(
            'Assets', 'drone.png')).convert_alpha(), (size * 100, size * 100))
    return SCALED_IMAGE


class Drone(Drawable, BaseMediator):
    lift: float = 22.5
    speed: float = 200

    status: DroneMode
    battery: Battery

    def __init__(self, grid_pos, name="",
                 logger: EventLogger = Provide[Container.event_logger],
                 env: Env = Provide[Container.env],
                 config=Provide[Container.config]):

        pygame.sprite.Sprite.__init__(self)

        self.speed = int(config["setup"]["drone_speed"])

        self.logger = logger
        self.env_ref = env
        self.battery = Battery()

        self.id = uuid.uuid4()
        self.status = DroneMode.IDLE
        self.name = name

        self.moves = []
        self.attachment = None
        self.curr_move = None

        self.size = 15

        self.grid_pos = grid_pos

        self.width = self.size
        self.height = self.size

        self.images = []
        msg = name + " initialized"
        self.logger.log(msg, False)
        self.images.append(get_scaled_image(self.size))
        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.vel = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2()

    def attach(self, task: Task):
        self.logger.log(self.name + " attach!")

        # if task.rect.x != self.rect.x or task.rect.y != self.rect.y:
        #     raise Exception('can not attach - drone is not centered over a package! 😤📦', self.name,
        #                     (self.rect.x, self.rect.y))

        self.attachment = task
        self.attachment.set_taken()
        self.battery.set_package(self.attachment.get_lift_requirement(),
                                 0.25, 0.25)

    ######
    def drop(self):

        if self.attachment is None:
            raise Exception('you can not drop a package you dont have!!!! 😤📦',
                            self.name, (self.rect.x, self.rect.y))

        # delivered bool
        self.logger.log(f"{self.name} - DROP, {self.attachment}")
        self.attachment = None
        self.battery.remove_package()

    def add_move_point(self, pos: Pos, name: Move_Type = Move_Type.NORMAL, obj: any = None):
        self.moves.append((pos, name, obj))

    def move_package_with_drone(self):

        if self.attachment is not None:
            self.attachment.rect.x = self.rect.x
            self.attachment.rect.y = self.rect.y

    def process_task(self, dt):
        if self.curr_move is None and len(self.moves) == 0 and self.status != DroneMode.IDLE:
            self.ready()  # send a ready signal to the drone controller
            self.status = DroneMode.IDLE

        if self.curr_move is not None:
            ay = self.rect.y
            ax = self.rect.x

            if get_move_type(self.curr_move) == Move_Type.HOME:
                point = self.env_ref.home

                bx = point[0]
                by = point[1]
            else:
                point = get_cor(self.curr_move)
                bx = point[0]
                by = point[1]

            self.do_move(ax, ay, bx, by, dt)

    def dock(self):
        self.status = DroneMode.DOCK

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

        ep = self.battery.update(dt, self.speed/14)
        #self.logger.log(self.name + " has inst power: {:.2f}".format(ep[1]))

    def do_move(self, ax, ay, bx, by, dt):
        self.move(ax, ay, bx, by, dt)

        # is we at the distinction?
        if ax == bx and ay == by or distance_between((ax, ay), (bx, by)) < 1:
            move_type = get_move_type(self.curr_move)

            if move_type == Move_Type.PICKUP:
                obj = get_move_obj(self.curr_move)
                self.attach(obj)
            elif move_type == Move_Type.DROP_OFF:
                self.drop()

            # TODO reimpliment drop zone check
            #  if not self.is_in_drop_zone():
            #     print(self.name + " did a drop of that was not in a drop zone 🤬.")

            self.curr_move = None

    def take_task(self):
        if len(self.moves) > 0 and self.curr_move is None:
            self.curr_move = self.moves.pop(0)
            self.status = DroneMode.BUSY
            self.logger.log(
                f"{self.name}, move to: ({'{0:.2f}'.format(self.curr_move[0][0])}, {'{0:.2f}'.format(self.curr_move[0][1])}) from: ({'{0:.2f}'.format(self.rect.x)}, {'{0:.2f}'.format(self.rect.y)})")

    def on_tick(self, delta):
        if self.status != DroneMode.DOCK:
            self.take_task()
            self.process_task(delta)
            self.move_package_with_drone()
        else:
            x, y = self.env_ref.home
            self.rect.x = x
            self.rect.y = y

    # not done (trying to turn the drone in the direction of flying)

    def is_in_drop_zone(self):
        return True
        # TODO change to new layout
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

    def ready(self):
        self.mediator.notify(self, "Ready")

    def __str__(self):
        return (f"{self.id}, {self.name} - {self.status}")

    def get_pos(self):
        return self.grid_pos

    def log_power(self):
        stat = self.battery.get_battery_stats()
        self.logger.log(self.name +
                        " average power: {:.2f} W".format(stat[0]))
        self.logger.log(self.name +
                        " energy consumption: {:.2f} J".format(stat[1]))
        self.logger.log(self.name +
                        " has done {:d} move ops in total.".format(stat[2]))
