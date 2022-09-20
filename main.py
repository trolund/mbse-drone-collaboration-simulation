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

drones = pygame.sprite.Group()
tasks = pygame.sprite.Group()
grounds = []


def get_task_at(x, y):
    return next((t for t in tasks if t.rect.x == x and t.rect.y == y), None)


def create_drones():
    drone = Drone()  # spawn player
    # start at x, y
    drone.rect.x = 200
    drone.rect.y = 200

    # movements
    drone.add_move_point(300, 300)
    drone.add_move_point(200, 200, Move_Type.PICKUP, get_task_at(200, 200))
    drone.add_move_point(300, 300)
    drone.add_move_point(900, 600)
    drone.add_move_point(100, 400, Move_Type.DROP_OFF)
    drone.add_move_point(900, 600)

    drones.add(drone)


def create_tasks():
    task = Task()  # spawn player
    # start at x, y
    task.rect.x = 200
    task.rect.y = 200

    tasks.add(task)


def create_grounds():
    grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (0, 0)))
    grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (700, 0)))
    grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (0, 700)))
    grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (700, 700)))


def draw_window():
    pygame.display.update()


def update_drones():
    for drone in drones:
        drone.update()


def create_env():
    create_tasks()
    create_drones()
    create_grounds()


def draw_layers():
    # draw grounds
    for g in grounds:
        g.draw(WIN)

    # draw tasks
    tasks.update()
    tasks.draw(WIN)

    # draw drones
    drones.update()
    drones.draw(WIN)


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
