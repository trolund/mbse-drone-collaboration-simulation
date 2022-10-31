import math


def calc_complexity(number_of_customers, world_size, delivery_sports, truck_pos, number_of_drones, number_of_tasks):
    total = sum(int(math.dist(pos, truck_pos)) for pos in delivery_sports)
    drone_package_raio = (number_of_tasks / number_of_drones)
    return world_size * number_of_customers * total * drone_package_raio * math.pow(10, -3)
