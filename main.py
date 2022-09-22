import pygame
import pygame_gui

# Basic setup
from Models.ground import Ground
from Models.move_type import Move_Type
from Models.task import Task
from UI import UI
from drone import Drone

pygame.init()
pygame.font.init()
pygame.mixer.init()

FPS = 60

WIDTH, HEIGHT = 1200, 1000

# WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("DRONE SIMULATION - MBSE - GROUP 2 (2022)")
pygame.font.Font(None, 22)
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class Env:
    drones = pygame.sprite.Group()
    tasks = pygame.sprite.Group()
    grounds: list[Ground] = []
    home = ((WIDTH / 2) - 30, (HEIGHT / 2) - 30)


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
    create_tasks()
    create_grounds()
    create_drones()


def draw_layers():
    # draw grounds
    for g in env.grounds:
        g.draw(WIN)

    # draw tasks
    env.tasks.update()
    env.tasks.draw(WIN)

    # draw drones
    env.drones.update()
    env.drones.draw(WIN)


def main():
    # instance of UI
    ui = UI(WIN)

    # create all objects in the environment
    create_env()

    # Simulation/game loop
    clock = pygame.time.Clock()
    run = True

    while run:
        time_delta = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            ui.handle_events(event)

        # clear background
        WIN.fill(WHITE)

        # draw object layers
        draw_layers()

        # update and draw UI
        ui.draw(time_delta)

        # update screen with drawing
        draw_window()


if __name__ == "__main__":
    main()
