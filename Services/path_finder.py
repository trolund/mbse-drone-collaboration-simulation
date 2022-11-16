import heapq
import numpy as np

from dependency_injector.wiring import Provide
#from sklearn.cluster import KMeans


from Models.basic_types import Pos
from containers import Container


# inspiration - https://www.analytics-link.com/post/2018/09/14/applying-the-a-path-finding-algorithm-in-python-part-1
# -2d-square-grid
class PatchFinder:

    def __init__(self, config=Provide[Container.config]):
        self.config = config

    def heuristic(self, a: Pos, b: Pos):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def astar(self, layout, start: Pos, goal: Pos):

        layout = np.array(layout)

        # can move diagonally
        # neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        # only move in 90deg
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        close_set = set()

        came_from = {}

        gscore = {start: 0}

        fscore = {start: self.heuristic(start, goal)}

        oheap = []

        heapq.heappush(oheap, (fscore[start], start))

        while oheap:

            current = heapq.heappop(oheap)[1]

            if current == goal:

                data = []

                while current in came_from:
                    data.append(current)

                    current = came_from[current]

                return data

            close_set.add(current)

            for i, j in neighbors:

                neighbor = current[0] + i, current[1] + j

                tentative_g_score = gscore[current] + self.heuristic(current, neighbor)

                if 0 <= neighbor[0] < layout.shape[0]:
                    if 0 <= neighbor[1] < layout.shape[1]:
                        if layout[neighbor[0]][neighbor[1]] != "R":
                            continue

                    else:
                        # array bound y walls
                        continue

                else:
                    # array bound x walls
                    continue

                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    came_from[neighbor] = current

                    gscore[neighbor] = tentative_g_score

                    fscore[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)

                    heapq.heappush(oheap, (fscore[neighbor], neighbor))

    def find_path(self, layout, start: Pos, goal: Pos):
        r = self.astar(layout, start, goal)
        r.reverse()

        route = []
        route.append(start)
        route.extend(r)
        route.append(goal)

        return route

    def compute_stop_points(self, route):

        nr_of_steps = len(route)
        nr_of_stops = int(float(self.config["setup"]["truck_stop_density"]) * nr_of_steps)

        stop_points = []
        slice = int(len(route) / nr_of_stops)
        index = 0
        for i in range(nr_of_steps):
            try:
                stop_points.append(route[index])
                index = index + slice
            except:
                break

        return stop_points




 