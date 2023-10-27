from .strike import RandomAlgorithm, BoundedInstance
import numpy as np


class Random(RandomAlgorithm):
    """
    Basic randomized algoithm, aka the "haha randint go brrrrr"-algorithm.
    """
    def setup(self) -> None:
        assert isinstance(self.I, BoundedInstance)
        rng = np.random.default_rng()
        self.decisions = [0] * self.I.m
        for i in rng.integers(0, self.I.m, size=self.I.n):
            self.decisions[i] += 1

    def decide(self, i: int, n_i: int, s_i: int, p_i: int, h_i: int) -> int:
        return self.decisions[i-1]
