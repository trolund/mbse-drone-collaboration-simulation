import heapq
import numpy as np

from Models.basic_types import Pos
from Utils.layout_utils import create_layout_env, print_layout


class PatchFinder:

    def heuristic(self, a: Pos, b: Pos):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def astar(self, layout, start: Pos, goal: Pos):

        layout = np.array(layout)

        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

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
        route = []
        route.append(start)
        route.append(planner.astar(layout, start, goal))
        route.append(goal)

        return route





if __name__ == "__main__":
    (layout, delivery_sports, number_of_grounds, number_of_customers), truck_pos = create_layout_env(
        200,
        10,
        2,
        0.2)

    planner = PatchFinder()

    route = planner.find_path(layout, (0, 0), (len(layout)-1, len(layout)-1))

    for i in range(len(layout)):
        print()
        for j in range(len(layout)):
            if (i, j) in route:
                layout[i][j] = "M"

    print_layout(layout)




