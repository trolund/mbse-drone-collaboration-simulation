from typing import List

from dependency_injector.wiring import Provide

from Logging.eventlogger import EventLogger
from Models.env import Env
from Models.task import Task
from Utils.layout_utils import distance_between
from containers import Container


class TaskManager:

    logger: EventLogger
    env_ref: Env

    def __init__(self, logger: EventLogger = Provide[Container.event_logger], config=Provide[Container.config], env: Env = Provide[Container.env]):

        self.config = config
        self.logger = logger
        self.env_ref = env

        # sort the packages
        # self.env_ref.task_ref = self.sort_tasks(env.task_ref)

    def get_number_of_packages_left(self):
        return len(self.env_ref.task_ref)

    def get_head_package(self):
        self.logger.log(f"packages left in que: {len(self.env_ref.task_ref)}", show_in_ui=False)
        return self.env_ref.task_ref.pop()

    def is_done(self):
        return len(self.env_ref.task_ref) == 0

    def sort_tasks(self, tasks: List[Task]):
        return sorted(tasks, key=lambda x: distance_between(self.env_ref.home, (x.rect.x, x.rect.y)))

    def print_tasks(self, tasks: List[Task], home):
        for t in tasks:
            print(distance_between(home, (t.rect.x, t.rect.y)))

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