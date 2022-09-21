import pygame

# Basic setup
from Models.ground import Ground
from Models.move_type import Move_Type
from Models.task import Task
from drone import Drone

pygame.font.init()
pygame.mixer.init()

FPS = 60

WIDTH, HEIGHT = 1200, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DRONE SIMULATION - MBSE - GROUP 2 (2022)")
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# Import resources
# DRONE_IMAGE = pygame.image.load(os.path.join('Assets', 'drone.svg'))
# DRONE = pygame.transform.rotate(pygame.transform.scale(DRONE_IMAGE, (DRONE_WIDTH, DRONE_HEIGHT)), 90)
class Env:
    drones = pygame.sprite.Group()
    tasks = pygame.sprite.Group()
    grounds = []
    home = (0, 0)

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
        drone.add_move_point(((HEIGHT / 2) + 75, 400 + (d * 60)), Move_Type.DROP_OFF)
        # drone.add_move_point(900, 600 * d)
        drone.add_move_point(env.home)

        env.drones.add(drone)


def create_tasks():
    for d in range(0, 4):
        task = Task()
        # start at x, y
        task.rect.x = 200 + (d * 60)
        task.rect.y = 200

        print(task.rect.x, task.rect.y)
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
    create_drones()
    create_grounds()


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
    # create all objects in the environment
    create_env()

    # Simulation/game loop
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # clear background
        WIN.fill(WHITE)

        # draw object layers
        draw_layers()

        # update screen with drawing
        draw_window()


if __name__ == "__main__":
    main()
