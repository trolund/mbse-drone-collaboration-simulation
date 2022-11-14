from typing import List

from dependency_injector.wiring import Provide
from scipy.spatial import distance

from Logging.eventlogger import EventLogger
from Models.env import Env
from Models.task import Task
from Utils.layout_utils import distance_between, grid_to_pos_tuple
from containers import Container


class TaskManager:

    logger: EventLogger
    env_ref: Env

    def __init__(self, step_size, logger: EventLogger = Provide[Container.event_logger], config=Provide[Container.config], env: Env = Provide[Container.env]):

        self.config = config
        self.logger = logger
        self.env_ref = env
        self.step_size = step_size

        # sort the packages
        self.env_ref.task_ref = self.sort_tasks(env.task_ref)

        self.delivery_clusters = None

    def get_number_of_packages_left(self):
        return len(self.env_ref.task_ref)

    def get_head_package(self):
        self.logger.log(f"Packages left in queue: {len(self.env_ref.task_ref)}", show_in_ui=False)
        return self.env_ref.task_ref.pop()

    def is_done(self):
        return len(self.env_ref.task_ref) == 0

    def sort_tasks(self, tasks: List[Task]):
        sorted_tasks = sorted(tasks, key=lambda x: distance_between(self.env_ref.home, grid_to_pos_tuple(x.address, self.step_size)), reverse=True)
        self.print_tasks(sorted_tasks, self.env_ref.home)
        return sorted_tasks

    def print_tasks(self, tasks: List[Task], home):
        for t in tasks:
            print(t.address, distance_between(self.env_ref.home, grid_to_pos_tuple(t.address, self.step_size)))

    def get_addr_of_tasks_left(self):
        tasks = self.env_ref.task_ref
        
        addresses = []
        for t in tasks:
            addresses.append(t.get_address())

        return addresses

    def cluster_delivery(self, cluster_centers, delivery_address):

        print("CLUSTER")
        print(cluster_centers)
        print(delivery_address)

        pack_clusters = [[] for i in range(len(cluster_centers))]

        for i in delivery_address:
            min_dist = distance.euclidean(i,cluster_centers[0])
            min_index =  0
            for m in range(len(cluster_centers)):
                dist = distance.euclidean(i,cluster_centers[m])
                if dist < min_dist:
                    min_dist = dist
                    min_index = m
            pack_clusters[min_index].append(i)

        print(pack_clusters)

        self.delivery_clusters = pack_clusters

    def update_curr_cluster(self):
        # if all delivered
        self.delivery_clusters.pop(0)

    def get_curr_cluster(self):
        # print("pack_clusters: ", self.delivery_clusters)

        return self.delivery_clusters[0]

    # def cluster_delivery(self, delivery_address, stop_points):

    #     nr_of_clusters = len(stop_points)

    #     delivery_address = [list(el) for el in delivery_address]

    #     kmeans = KMeans(n_clusters=nr_of_clusters, init=stop_points)
    #     kmeans.fit(delivery_address)

    #     cluster_centers = kmeans.cluster_centers_

    #     print("cluster_centers: ", cluster_centers)
    #     print("stop_points: ", stop_points)

    #     clusters = [[] for i in range(nr_of_clusters)]
    #     index = 0

    #     for i in kmeans.labels_:
    #         clusters[i].append(delivery_address[index])
    #         index = index + 1

    #     return clusters, cluster_centers

    # def cluster_packages_kmeans(self, delivery_address, route):

    #     nr_of_clusters = self.compute_stop_points(route)

    #     delivery_address = [list(el) for el in delivery_address]

    #     kmeans = KMeans(n_clusters=nr_of_clusters)
    #     kmeans.fit(delivery_address)

    #     cluster_centers = kmeans.cluster_centers_

    #     clusters = [[] for i in range(nr_of_clusters)]
    #     index = 0

    #     for i in kmeans.labels_:
    #         clusters[i].append(delivery_address[index])
    #         index = index + 1

    #     return clusters, cluster_centers


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