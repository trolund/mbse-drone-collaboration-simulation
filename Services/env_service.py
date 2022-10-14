import math
import random

import pygame

from basic_types import Layout


def grid_to_pos(i, j, step_size):
    return step_size * i, step_size * j


def pos_to_grid(i, j, step_size):
    x, y = i / step_size, j / step_size
    return math.floor(x % step_size), math.floor(y % step_size)


def translate_moves(list: list[(int, int)], step_size: int):
    moves = []
    for p in list:
        moves.append(grid_to_pos(p[0], p[1], step_size))

    return moves


def safe_list_get(l, x, y):
    try:
        return l[x][y], (x, y)
    except IndexError:
        return "#", (0, 0)


def create_world(len):
    world = []
    for i in range(0, len):
        world.append(pygame.sprite.Group())

    return world


def add_offset(pos: (int, int), step_size):
    return pos[0] + step_size / 2, pos[1] + step_size / 2


def get_world_size(surface, layout):
    space = min(surface.get_height(), surface.get_width())

    x_len = len(layout)
    y_len = len(layout[0])

    step_size = space / x_len

    return step_size, x_len, y_len


def draw_env(surface, layout, x_len: int, y_len: int, step_size: int):
    # draw grounds
    for i in range(0, y_len):
        for j in range(0, x_len):
            color = 50 if (i + j) % 2 == 0 else 150
            x, y = grid_to_pos(i, j, step_size)

            if layout[i][j] == "R":
                pygame.draw.rect(surface, (200, 100, 100), pygame.Rect(x, y, step_size, step_size))
            elif layout[i][j] == "S":
                pygame.draw.rect(surface, (100, 10, 10),
                                 pygame.Rect(x, y, int(step_size),
                                             int(step_size)))
            elif layout[i][j] == ".":
                pygame.draw.rect(surface, (50, 10, 240),
                                 pygame.Rect(x, y, int(step_size),
                                             int(step_size)))
            else:
                pygame.draw.rect(surface, (color, 220, 222),
                                 pygame.Rect(x, y, int(step_size),
                                             int(step_size)))


def create_layout_env(world_size: int, ground_size: int, road_size: int = 2):
    m = world_size + road_size
    g = ground_size

    layout: Layout = [[""] * m for i in range(m)]

    for i in range(m):
        for j in range(m):
            if i % g < road_size:
                layout[i][j] = "R"  # Horizontal roads
            else:
                if j % g < road_size:  # vertical roads
                    layout[i][j] = "R"
                else:
                    layout[i][j] = "."

    return provide_dp(layout, m, ground_size, road_size)


def provide_dp(layout: Layout, world_size: int, ground_size: int, road_size: int):
    size = ground_size - road_size

    for i in range(road_size, world_size, ground_size):
        for j in range(road_size, world_size, ground_size):
            x = math.floor(random.uniform(i, i + size))
            y = math.floor(random.uniform(j, j + size))

            layout[x][y] = "S"

    return layout


def print_layout(layout: Layout):
    for i in range(len(layout)):
        print()
        for j in range(len(layout)):
            print(f' {layout[i][j]} ', end="")


if __name__ == "__main__":
    layout = create_layout_env(200, 10)
    print_layout(layout)
