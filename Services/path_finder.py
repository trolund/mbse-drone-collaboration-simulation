import heapq
import numpy as np

from Models.basic_types import Pos


# inspiration - https://www.analytics-link.com/post/2018/09/14/applying-the-a-path-finding-algorithm-in-python-part-1
# -2d-square-grid
class PatchFinder:

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


# if __name__ == "__main__":
#     (layout, delivery_sports, number_of_grounds, number_of_customers), truck_pos = create_layout_env(
#         world_size=15,
#         ground_size=5,
#         road_size=1,
#         customer_density=0.5)
#
#     planner = PatchFinder()
#
#     route = planner.find_path(layout, (0, 0), (len(layout) - 1, len(layout) - 1))
#
#     print(route)
#
#     for i in range(len(layout)):
#         for j in range(len(layout)):
#             if (i, j) in route:
#                 layout[i][j] = "M"
#
#     print_layout(layout)
