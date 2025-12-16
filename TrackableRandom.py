import random


class TrackableRandom:
    def __init__(self, seed):
        self._current_seed = seed
        random.seed(seed)

    def seed(self, seed):
        self._current_seed = seed
        random.seed(seed)
        return seed

    def get_current_seed(self):
        return self._current_seed

    def random(self):
        return self.seed(random.random())

    def randint(self, a, b):
        return self.seed(random.randint(a, b))