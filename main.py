import sys

import pygame
from dependency_injector.wiring import inject, Provide

from Logging.eventlogger import EventLogger
from Models.colors import WHITE
from Models.env import Env
# Basic setup
from Models.ground import Ground
from Models.move_type import Move_Type
from Models.setup import FPS
from Models.task import Task
from GUI.UI import UI
from Models.drone import Drone
from Models.truck import Truck
from Services.BaseService import UserService
from containers import Container

pygame.init()
pygame.font.init()
pygame.mixer.init()

# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("DRONE SIMULATION - MBSE - GROUP 2 (2022)")
pygame.font.Font(None, 22)

env = Env()


def get_task_at(x, y):
    return next((t for t in env.tasks if t.rect.x == x and t.rect.y == y), None)


def create_drones():
    for d in range(0, 4):
        drone = Drone(env, "done_" + str(d))
        # start at x, y
        drone.rect.x = 0
        drone.rect.y = 0

        # movements
        # drone.add_move_point(300, 300)
        drone.add_move_point((200 + (d * 60), 200), Move_Type.PICKUP, get_task_at(200 + (d * 60), 200))
        # drone.add_move_point(300 * d, 300)
        # drone.add_move_point(900, 600 * d)
        drone.add_move_point(env.grounds[d].get_landing_spot_pos(True), Move_Type.DROP_OFF)
        # drone.add_move_point(900, 600 * d)
        drone.add_move_point((env.home[0], env.home[1] + (d * 70)))

        env.drones.add(drone)


def create_tasks():
    for d in range(0, 4):
        task = Task()
        # start at x, y
        task.rect.x = 200 + (d * 60)
        task.rect.y = 200

        env.tasks.add(task)


def create_grounds():
    env.grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (0, 0)))
    env.grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (700, 0)))
    env.grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (0, 700)))
    env.grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (700, 700)))


def draw_window():
    pygame.display.update()


def update_drones():
    for drone in env.drones:
        drone.update()


def create_env():
    truck = Truck()
    env.trucks.add(truck)
    create_tasks()
    create_grounds()
    create_drones()


def draw_layers():
    # draw grounds
    for g in env.grounds:
        g.draw(WIN)

    # draw truck
    env.trucks.update()
    env.trucks.draw(WIN)

    # draw tasks
    env.tasks.update()
    env.tasks.draw(WIN)

    # draw drones
    env.drones.update()
    env.drones.draw(WIN)


@inject
def main(logger: EventLogger = Provide[Container.event_logger]):

    # instance of UI
    ui = UI(WIN)

    # create all objects in the environment
    create_env()

    # Simulation/game loop
    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()

            ui.handle_events(event)

        # clear background
        WIN.fill(WHITE)

        # draw object layers
        draw_layers()

        # update and draw UI
        ui.update(time_delta, clock.get_fps())

        # update screen with drawing
        draw_window()


if __name__ == "__main__":
    # setup dependency injection
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main(*sys.argv[1:])
