import pygame

# Basic setup
from Models.ground import Ground
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
grounds = []


def create_drones():
    player = Drone()  # spawn player
    # start at x, y
    player.rect.x = 200
    player.rect.y = 200

    # movements
    player.add_coordinates(300, 300)
    player.add_coordinates(900, 600)
    player.add_coordinates(100, 400)

    drones.add(player)

def create_Grounds():
    grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (0, 0)))
    grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (700, 0)))
    grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (0, 700)))
    grounds.append(Ground([(0, 0), (0, 500), (500, 500), (500, 0)], (700, 700)))


def draw_window():
    pygame.display.update()


def update_drones():
    for drone in drones:
        drone.update()


def main():
    create_drones()
    create_Grounds()

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

        # draw grounds
        for g in grounds:
            g.draw(WIN)

        # draw drones
        drones.update()
        drones.draw(WIN)

        draw_window()

    main()


if __name__ == "__main__":
    main()
