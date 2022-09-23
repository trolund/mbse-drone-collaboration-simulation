import sys

import pygame
from dependency_injector.wiring import inject, Provide

from GUI.UI import UI
from Logging.eventlogger import EventLogger
from Models.colors import WHITE
from Models.env import Env
from Models.env_builder import EnvBuilder
# Basic setup
from Models.setup import FPS
from containers import Container

pygame.init()
pygame.font.init()
pygame.mixer.init()

# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("DRONE SIMULATION - MBSE - GROUP 2 (2022)")
pygame.font.Font(None, 22)


def draw_window():
    pygame.display.update()


def update_drones(env: Env):
    for drone in env.drones:
        drone.update()


def draw_layers(env: Env):
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
def main(env: Env = Provide[Container.env]):

    # instance of UI
    ui = UI(WIN)

    # create all objects in the environment
    EnvBuilder().create_env()

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
        draw_layers(env)

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
