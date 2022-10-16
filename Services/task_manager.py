import random

from Models.package import Package
from Models.task import Task


# def queue_package(amount_of_packages, possible_addresses, max_weight):
#     min_weight = 200
#     queue = []
#
#     for i in range(amount_of_packages):
#         if min_weight == max_weight:
#             weight = min_weight
#         else:
#             weight = random.randrange(min_weight, max_weight)
#         point = random.randrange(0, len(possible_addresses))
#         address = possible_addresses[point]
#         del possible_addresses[point]
#         package = Task(weight, address)
#         queue.append(package)
#     return queue

def create_packages(amount_of_packages, max_weight):
    min_weight = 200
    packages = []

    for i in range(amount_of_packages):
        if min_weight == max_weight:
            weight = min_weight
        else:
            weight = random.randrange(min_weight, max_weight)

        package = Package(weight)
        packages.append(package)

    return packages


def get_random_address(possible_addresses):
    index = random.randrange(0, len(possible_addresses))
    return possible_addresses[index]


def create_random_tasks(possible_addresses, number_of_tasks):
    tasks = []

    for i in range(number_of_tasks):
        point = get_random_address(possible_addresses)
        packages = create_packages(1, 200)
        t = Task(point, packages)
        tasks.append(t)

    return tasks

# if __name__ == "__main__":
#     possible_addresses = [[1,1],[2,2],[3,3],[4,4]]
#     amount_of_packages = 3
#     max_weight = 200
#     queue = queue_package(amount_of_packages,possible_addresses,max_weight)
#     for i in queue:
#         print(i)
