import pygame
import os

# Basic setup
pygame.font.init()
pygame.mixer.init()

FPS = 60
DRONE_WIDTH, DRONE_HEIGHT = 55, 40

WIDTH, HEIGHT = 1200, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DRONE SIMULATION - MBSE - GROUP 2 (2022)")
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# Import resources
DRONE_IMAGE = pygame.image.load(os.path.join('Assets', 'drone.svg'))
DRONE = pygame.transform.rotate(pygame.transform.scale(DRONE_IMAGE, (DRONE_WIDTH, DRONE_HEIGHT)), 90)


def draw_window():
    WIN.blit(DRONE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    pygame.display.update()


def main():
    # Simulation/game loop
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        draw_window()

    main()


if __name__ == "__main__":
    main()
