import random

class Random_util:

    seed = 0

    def __init__(self, seed):
        self.seed = seed
        random.seed(seed)

    def get_rand(self, r_min, r_max):
        return random.uniform(r_min, r_max)

    def get_seed(self):
        return self.seed
