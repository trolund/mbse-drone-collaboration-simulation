import pygame
import pygame_gui

# Basic setup
from Models.ground import Ground
from Models.move_type import Move_Type
from Models.task import Task
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

# UI
UI_WIDTH = 400
UI_X = WIN.get_width() - UI_WIDTH



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

    margin = 30
    ui_x = UI_X + margin

    manager = pygame_gui.UIManager((WIN.get_width(), WIN.get_height()))

    button1 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(ui_x, 400, 100, 30),
        text='Click me 1',
        manager=manager
    )

    button2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(ui_x, 200, 100, 30),
        text='Click me 2',
        manager=manager
    )

    label1 = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(ui_x, 100, 200, 100),
        text="Value",
        manager=manager
    )

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

            if event.type == pygame.USEREVENT:
                if event.ui_element == button1:
                        label1.set_text("click 1")
                        print("click 1")
                if event.ui_element == button2:
                        label1.set_text("click 2")
                        print("click 2")

                manager.process_events(event)
        # clear background
        WIN.fill(WHITE)

        # draw object layers
        draw_layers()

        # update and draw UI
        pygame.draw.rect(WIN, (220, 220, 222), pygame.Rect(UI_X, 0, UI_WIDTH, WIN.get_height()))
        manager.update(time_delta)
        manager.draw_ui(WIN)

        # update screen with drawing
        draw_window()


if __name__ == "__main__":
    main()
