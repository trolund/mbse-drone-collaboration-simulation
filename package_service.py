import math
import sys
from typing import List


def distance_between(a, b):
    return math.dist(a, b)

"""Return the package with the smallest distance from home (truck) to the destination"""
def get_package_best_package(addresses: List[(int, int)], home: (int, int)):
    best = None
    min_dist = sys.maxint

    for a in addresses:
        curr_dist = distance_between(home, a)

        if curr_dist < min_dist:
            min_dist = curr_dist
            best = a

    return best