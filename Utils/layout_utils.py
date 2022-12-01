import math
import pygame

from Models.basic_types import Layout, Pos
from Models.colors import GREY, GREEN, GREENY, DARK_GERY
from Utils.Random_utils import Random_util


def grid_to_pos(i, j, step_size, scale: float = 1.0):
    return step_size * i * scale, step_size * j * scale


def grid_to_pos_tuple(pos: Pos, step_size, scale: float = 1.0):
    return grid_to_pos(pos[0], pos[1], step_size, scale)


def pos_to_grid(i, j, step_size, scale: float = 1.0):
    x, y = (i / step_size) / scale, (j / step_size) / scale
    return math.floor(x), math.floor(y)


def pos_to_grid_tuple(pos: Pos, step_size, scale: float = 1.0):
    return pos_to_grid(pos[0], pos[1], step_size, scale)


def translate_moves(arr: list[Pos], step_size: int, scale: float = 1.0):
    moves = []
    for p in arr:
        moves.append(grid_to_pos(p[0], p[1], step_size, scale))

    return moves


def safe_list_get(arr, x, y):
    try:
        return arr[x][y], (x, y)
    except IndexError:
        return "#", (0, 0)


def create_world(length):
    world = []
    for i in range(0, length):
        world.append(pygame.sprite.Group())

    return world


def add_offset(pos: (int, int), step_size):
    return pos[0] + step_size / 2, pos[1] + step_size / 2


def get_world_size(surface: pygame.Surface, layout: Layout):
    init_size = 50 * len(layout)

    scale = min(surface.get_height(), surface.get_width()) / init_size

    x_len = len(layout)
    y_len = len(layout[0])

    step_size = init_size / x_len

    return step_size, x_len, y_len, scale


def scale_corr(cor: Pos, scale: float):
    return cor[0] * scale, cor[1] * scale


def offset_corr(cor: Pos, offset_x: int = 0, offset_y: int = 0):
    return cor[0] + offset_x, cor[1] + offset_y


def draw_layout(surface, layout, x_len: int, y_len: int, step_size: int, scale: float = 1, offset_x: int = 0,
                offset_y: int = 0):
    # draw grounds
    for i in range(0, y_len):
        for j in range(0, x_len):

            x, y = offset_corr(scale_corr(grid_to_pos(
                i, j, step_size), scale), offset_x, offset_y)
            size = (step_size * scale) + 1

            if layout[i][j] == "R":
                pygame.draw.rect(surface, DARK_GERY,
                                 pygame.Rect(x, y, size, size))
            elif layout[i][j] == "S":
                pygame.draw.rect(
                    surface, GREENY, pygame.Rect(x, y, size, size))
            elif layout[i][j] == ".":
                pygame.draw.rect(surface, GREEN, pygame.Rect(x, y, size, size))
            else:
                pygame.draw.rect(surface, GREY, pygame.Rect(x, y, size, size))


def create_layout_env(world_size: int,
                      ground_size: int,
                      rand: Random_util,
                      road_size: int = 2,
                      customer_density: float = 0.5,
                      moving_truck: bool = True,
                      random_position: bool = False
                      ):

    m = world_size + road_size
    g = ground_size

    layout: Layout = [[""] * m for _ in range(m)]

    for i in range(m):
        for j in range(m):
            if i % g < road_size:
                layout[i][j] = "R"  # Horizontal roads
            else:
                if j % g < road_size:  # vertical roads
                    layout[i][j] = "R"
                else:
                    layout[i][j] = "."

    # Options:
    # moving_truck = 1 -> the truck moves
    # moving_truck = 0 and random_position = 0 -> stationary truck with the optimal position
    # moving_truck = 0 and random_position = 1 -> stationary truck with the random position

    if moving_truck == False and random_position == False:
        layout, delivery_spots, number_of_grounds, number_of_customers = provide_dp(
            layout, rand, m, ground_size, road_size, customer_density)
        new_layout, truck_pos = find_optimal_truck_pos(layout, delivery_spots)
        return [new_layout, delivery_spots, number_of_grounds, number_of_customers], truck_pos

    elif moving_truck == False and random_position == True:
        layout, delivery_spots, number_of_grounds, number_of_customers = provide_dp(
            layout, rand, m, ground_size, road_size, customer_density)
        new_layout, truck_pos = find_random_truck_pos(layout, rand)
        return [new_layout, delivery_spots, number_of_grounds, number_of_customers], truck_pos
    else:
        return provide_dp(layout, rand, m, ground_size, road_size, customer_density), (0, 0)


def find_optimal_truck_pos(layout: Layout, pack_pos):

    road_pos = find_all_road_pos(layout)
    pos_length = len(pack_pos)
    n = pos_length - 1

    xcords = sorted(list(list(zip(*pack_pos))[0]))
    ycords = sorted(list(list(zip(*pack_pos))[1]))

    if len(pack_pos) % 2 != 0:
        x = xcords[int((n+1)/2)]
        y = ycords[int((n+1)/2)]
    else:
        # print(type(int(n/2)+1))
        x = int((xcords[int(n/2)] + xcords[int(n/2)+1]) / 2)
        y = int((ycords[int(n/2)] + ycords[int(n/2)+1]) / 2)

    med_package_pos = (x, y)

    pos = min(road_pos, key=lambda c: (
        c[0] - med_package_pos[0])**2 + (c[1]-med_package_pos[1])**2)

    return layout, pos


def distance(co1, co2):
    return math.sqrt(pow(abs(co1[0] - co2[0]), 2) + pow(abs(co1[1] - co2[2]), 2))


def find_all_road_pos(layout):

    pos = []
    for i in range(len(layout)):
        for j in range(len(layout[0])):
            if (layout[i][j] == "R"):
                pos.append(tuple((i, j)))

    return pos


def find_random_truck_pos(layout: Layout, rand: Random_util):
    pos = find_random_road_pos(layout, rand)
    # layout[pos[0]][pos[1]] = "T"
    return layout, pos


def find_random_road_pos(layout: Layout, rand: Random_util):

    curr = None
    pos = (0, 0)
    while curr != "R":
        length = len(layout)
        x = math.floor(rand.get_rand(0, length))
        y = math.floor(rand.get_rand(0, length))

        curr = layout[x][y]
        pos = (x, y)

    return pos


def provide_dp(layout: Layout,
               rand: Random_util,
               world_size: int,
               ground_size: int,
               road_size: int,
               change_of_customer: float):
    delivery_spots = []
    number_of_grounds = 0
    number_of_customers = 0

    size = ground_size - road_size

    for i in range(road_size, world_size, ground_size):
        for j in range(road_size, world_size, ground_size):
            # change of the ground being signed up for delivery
            if rand.get_rand(0, 1) < change_of_customer:
                # assign the delivery spot to a random point on the ground
                x = math.floor(rand.get_rand(i, i + size))
                y = math.floor(rand.get_rand(j, j + size))
                number_of_customers += 1

                # add address to list
                delivery_spots.append((x, y))

                layout[x][y] = "S"

            number_of_grounds += 1

    return layout, delivery_spots, number_of_grounds, number_of_customers


def print_layout(layout: Layout):
    for i in range(len(layout)):
        print()
        for j in range(len(layout)):
            print(f' {layout[i][j]} ', end="")

    print()


def distance_between(a, b):
    return math.dist(a, b)
