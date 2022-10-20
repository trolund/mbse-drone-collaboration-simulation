import random
from typing import List

import math
from dependency_injector.wiring import Provide

from Logging.eventlogger import EventLogger
from Models.env import Env
from Models.package import Package
from Models.task import Task
from containers import Container


class TaskManager:

    logger: EventLogger
    env_ref: Env

# tasks: List[Task], delivery_addresses
    def __init__(self, logger: EventLogger = Provide[Container.event_logger], config=Provide[Container.config], env: Env = Provide[Container.env]):

        self.config = config
        self.logger = logger
        self.env_ref = env

    def distance_between(self, a, b):
        return math.dist(a, b)

    def create_packages(self, amount_of_packages, max_weight):
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

    def get_random_address(self, possible_addresses):
        index = random.randrange(0, len(possible_addresses))
        return possible_addresses[index]

    def create_random_tasks(self, possible_addresses, number_of_tasks):
        tasks = []

        for i in range(number_of_tasks):
            point = self.get_random_address(possible_addresses)
            packages = self.create_packages(1, 200)
            t = Task(point, packages)
            tasks.append(t)

        return tasks

    def sort_tasks(self, tasks: List[Task]):
        return sorted(tasks, key=lambda x: self.distance_between(self.env_ref.home, (x.rect.x, x.rect.y)))

    def print_tasks(self, tasks: List[Task], home):
        for t in tasks:
            print(self.distance_between(home, (t.rect.x, t.rect.y)))

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



# if __name__ == "__main__":
#     possible_addresses = [[1,1],[2,2],[3,3],[4,4]]
#     amount_of_packages = 3
#     max_weight = 200
#     queue = queue_package(amount_of_packages,possible_addresses,max_weight)
#     for i in queue:
#         print(i)


"""Return the package with the smallest distance from home (truck) to the destination"""


# def get_package_best_package(addresses: List[(int, int)], home: (int, int)):
#     best = None
#     min_dist = sys.maxint
#
#     for a in addresses:
#         curr_dist = distance_between(home, a)
#
#         if curr_dist < min_dist:
#             min_dist = curr_dist
#             best = a
#
#     return best