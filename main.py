import sys

import pygame
import pygame_gui
from dependency_injector.wiring import inject, Provide
from pygame.event import Event

from Models.basic_types import Pos
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
from Services.env_service import draw_layout, create_layout_env, get_world_size, grid_to_pos, pos_to_grid
from containers import Container

pygame.init()
pygame.font.init()
pygame.mixer.init()

# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN: pygame.Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCALE: int = 1
TRUCK_POS_RANDOM: bool = False
FIXED_TRUCK_POS: Pos = (0, 0)


OffsetX = 0
OffsetY = 0

is_running = True

pygame.display.set_caption("DRONE SIMULATION - MBSE - GROUP 2 (2022)")
pygame.font.Font(None, 22)


def create_drones(env: Env):
    for d in range(0, 4):
        drone = Drone(SCALE, "done_" + str(d))
        # start at x, y
        drone.rect.x = 0
        drone.rect.y = 0

        # movements
        # drone.add_move_point(300, 300)
        drone.add_move_point((200 + (d * 60), 200), Move_Type.PICKUP, env.get_task_at(200 + (d * 60), 200))
        # drone.add_move_point(300 * d, 300)
        # drone.add_move_point(900, 600 * d)
        drone.add_move_point(env.grounds[d].get_landing_spot_pos(offset=True), Move_Type.DROP_OFF)
        # drone.add_move_point(900, 600 * d)
        drone.add_move_point((env.home[0], env.home[1] + (d * 70)))

        env.drones.add(drone)


def create_tasks(env: Env):
    for d in range(0, 4):
        task = Task()
        # start at x, y
        task.rect.x = 200 + (d * 60)
        task.rect.y = 200

        env.tasks.add(task)


# def create_grounds(env: Env):
#     env.grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (0, 0)))
#     env.grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (700, 0)))
#     env.grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (0, 700)))
#     env.grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (700, 700)))


def draw_window():
    pygame.display.update()


def update_drones(env: Env):
    for drone in env.drones:
        drone.update()


def create_truck(env: Env, pos):
    truck = Truck(pos, SCALE)
    env.home = truck.get_home()
    env.trucks.add(truck)


def create_env(env: Env):
    print("create")
    #create_tasks(env)
    #create_grounds(env)
    #create_drones(env)





def draw_layers(layout, x_len: int, y_len: int, step_size: int, env):
    # draw the basic layout
    draw_layout(WIN, layout, x_len, y_len, step_size, SCALE, OffsetX, OffsetY)

    # draw truck
    env.trucks.update(SCALE)

    for t in env.trucks:
        WIN.blit(t.image, [(t.rect.x + OffsetX), (t.rect.y + OffsetY)])


    #
    # draw tasks
    env.tasks.update()
    env.tasks.draw(WIN)
    #
    # draw drones
    env.drones.update(SCALE)
    env.drones.draw(WIN)




def set_scale(val):
    global SCALE
    temp = SCALE + val
    if temp < 1:
        SCALE = 1
    else:
        SCALE = temp


def get_config(config):
    global SCALE
    global FIXED_TRUCK_POS
    global TRUCK_POS_RANDOM

    SCALE = float(config["setup"]["scale"])
    TRUCK_POS_RANDOM = bool(config["setup"]["truck_pos_random"])
    a = config["setup"]["fixed_truck_pos"].split(",")
    FIXED_TRUCK_POS = (int(a[0]), int(a[1]))

def keyboard_input():
    global OffsetX
    global OffsetY

    keys = pygame.key.get_pressed()  # checking pressed keys
    if keys[pygame.K_LEFT]:
        OffsetX += 5
    if keys[pygame.K_RIGHT]:
        OffsetX -= 5
    if keys[pygame.K_UP]:
        OffsetY += 5
    if keys[pygame.K_DOWN]:
        OffsetY -= 5

    # if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
    #     if event.mod == pygame.KMOD_NONE:

        # else:
        #     if event.mod & pygame.KMOD_LSHIFT:
        #         print('Left shift was in a pressed state when this event '
        #               'occurred.')
        #     if event.mod & pygame.KMOD_RSHIFT:
        #         print('Right shift was in a pressed state when this event '
        #               'occurred.')
        #     if event.mod & pygame.KMOD_SHIFT:
        #         print('Left shift or right shift or both were in a '
        #               'pressed state when this event occurred.')


@inject
def main(env: Env = Provide[Container.env], config=Provide[Container.config]):
    global is_running

    get_config(config)

    # setup layout
    (layout, delivery_sports, number_of_grounds, number_of_customers), truck_pos = create_layout_env(50, 10,
                                                                                                     change_of_customer=1.0)
    (step_size, x_len, y_len) = get_world_size(WIN, layout)

    # instance of UI
    ui = UI(set_scale, WIN)

    is_paused = True

    pause_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(WIN.get_width() - 400, WIN.get_height() - 40, 100, 30),
        text="▶ Start",
        manager=ui.get_manager()
    )

    # create all objects in the environment
    create_truck(env, grid_to_pos(truck_pos[0], truck_pos[1], step_size, SCALE))
    create_env(env)

    # Simulation/game loop
    clock = pygame.time.Clock()


    while is_running:
        time_delta = clock.tick(FPS) / 1000.0
        keyboard_input()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == pause_btn:
                        is_paused = not is_paused
                        pause_btn.set_text("▶ Resume" if is_paused else "Pause")


            ui.handle_events(event)

        if not is_paused:
            # clear background
            WIN.fill(WHITE)

            # draw object layers

            draw_layers(layout, x_len, y_len, step_size, env)

        # update and draw UI
        ui.update(time_delta, clock.get_fps(), SCALE)

        # apply offsets
        #offset_sprites(env)
        pygame.display.flip()

        # update screen with drawing
        draw_window()


    pygame.quit()


if __name__ == "__main__":
    # setup dependency injection
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main(*sys.argv[1:])
