import math
import random

import pygame

from Models.basic_types import Layout
from Models.colors import GREY, GREEN, GREENY, DARK_GERY


def grid_to_pos(i, j, step_size, scale: float = 1.0):
    return step_size * i * scale, step_size * j * scale


def pos_to_grid(i, j, step_size, scale: float = 1.0):
    x, y = (i / step_size) / scale, (j / step_size) / scale
    return math.floor(x), math.floor(y)


def translate_moves(list: list[(int, int)], step_size: int, scale: float = 1.0):
    moves = []
    for p in list:
        moves.append(grid_to_pos(p[0], p[1], step_size, scale))

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


def get_world_size(surface: pygame.Surface, layout: Layout):
    space = min(surface.get_height(), surface.get_width())

    x_len = len(layout)
    y_len = len(layout[0])

    step_size = space / x_len

    return step_size, x_len, y_len


def scale_corr(cor: (int, int), scale: float):
    return cor[0] * scale, cor[1] * scale


def offset_corr(cor: (int, int), offset_x: int = 0, offset_y: int = 0):
    return cor[0] + offset_x, cor[1] + offset_y


def draw_layout(surface, layout, x_len: int, y_len: int, step_size: int, scale: float = 1, offset_x: int = 0,
                offset_y: int = 0):
    # draw grounds
    for i in range(0, y_len):
        for j in range(0, x_len):

            x, y = offset_corr(scale_corr(grid_to_pos(i, j, step_size), scale), offset_x, offset_y)
            size = (step_size * scale) + 1

            if layout[i][j] == "R":
                pygame.draw.rect(surface, DARK_GERY, pygame.Rect(x, y, size, size))
            elif layout[i][j] == "S":
                pygame.draw.rect(surface, GREENY, pygame.Rect(x, y, size, size))
            elif layout[i][j] == ".":
                pygame.draw.rect(surface, GREEN, pygame.Rect(x, y, size, size))
            else:
                pygame.draw.rect(surface, GREY, pygame.Rect(x, y, size, size))


def create_layout_env(world_size: int, ground_size: int, road_size: int = 2, change_of_customer: float = 0.5,
                      random_truck_pos: bool = False):
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

    if random_truck_pos:
        new_layout, truck_pos = create_random_truck_pos(layout)
        return provide_dp(new_layout, m, ground_size, road_size, change_of_customer), truck_pos
    else:
        return provide_dp(layout, m, ground_size, road_size, change_of_customer), (0, 0)


def create_random_truck_pos(layout: Layout):
    pos = find_random_road_pos(layout)
    layout[pos[0]][pos[1]] = "T"
    return layout, pos


def find_random_road_pos(layout: Layout):
    curr = None
    pos = (0, 0)
    while curr != "R":
        length = len(layout)
        x = math.floor(random.uniform(0, length))
        y = math.floor(random.uniform(0, length))

        curr = layout[x][y]
        pos = (x, y)

    return pos


def provide_dp(layout: Layout, world_size: int, ground_size: int, road_size: int, change_of_customer: float):
    delivery_sports = []
    number_of_grounds = 0
    number_of_customers = 0

    size = ground_size - road_size

    for i in range(road_size, world_size, ground_size):
        for j in range(road_size, world_size, ground_size):
            if random.uniform(0, 1) < change_of_customer:  # change of the ground being signed up for delivery
                # assign the delivery spot to a random point on the ground
                x = math.floor(random.uniform(i, i + size))
                y = math.floor(random.uniform(j, j + size))
                number_of_customers += 1

                # add address to list
                delivery_sports.append((x, y))

                layout[x][y] = "S"

            number_of_grounds += 1

    return layout, delivery_sports, number_of_grounds, number_of_customers


def print_layout(layout: Layout):
    for i in range(len(layout)):
        print()
        for j in range(len(layout)):
            print(f' {layout[i][j]} ', end="")

    print()

# if __name__ == "__main__":
#     (layout, delivery_sports, number_of_grounds, number_of_customers), truck_pos = create_layout_env(15, 5, 1, 0.5)
#     print_layout(layout)
#     print(number_of_customers, number_of_grounds, truck_pos, delivery_sports)
