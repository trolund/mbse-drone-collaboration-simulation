import random

from Models.package import Package
from Models.task import Task


def get_random_address(possible_addresses):
    index = random.randrange(0, len(possible_addresses))
    return possible_addresses[index]


def create_packages(amount_of_packages, min_weight, max_weight):
    packages = []

    for i in range(amount_of_packages):
        if min_weight == max_weight:
            weight = min_weight
        else:
            weight = random.randrange(min_weight, max_weight)

        package = Package(weight)
        packages.append(package)

    return packages


def create_random_tasks(possible_addresses, number_of_tasks, min_weight, max_weight, load_img=True):
    tasks = []

    for i in range(number_of_tasks):
        point = get_random_address(possible_addresses)
        packages = create_packages(1, min_weight, max_weight)
        t = Task(point, packages, load_img=load_img)
        tasks.append(t)

    return tasks
