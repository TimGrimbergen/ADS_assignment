from .strike import BoundedInstance, Algorithm
import numpy as np


class FastGreedy(Algorithm):
    def setup(self):
        assert isinstance(self.I, BoundedInstance)
        self.p_max = self.I.p_max
        self.p_min = self.I.p_max
        self.CC = 0

    def decide(self, i: int, n_i: int, s_i: int, p_i: int, h_i: int) -> int:
        if i == self.I.m:
            return min(n_i, s_i)
        self.p_min = min(self.p_min, p_i)
        numer = (self.p_max - self.p_min) * n_i - (self.p_min - 1) * self.CC
        denum = self.p_max + p_i * self.p_min - p_i - self.p_min
        f_est = max(0, numer / denum) if denum != 0 else n_i
        worst_cost = (lambda f_i:
            max((self.CC + p_i * f_i + self.p_max * (n_i - f_i)) / (self.p_min * self.I.n),
                (self.CC + p_i * f_i + n_i - f_i) / self.I.n))
        if worst_cost(f_floor := np.floor(f_est)) < worst_cost(f_ceil := np.ceil(f_est)):
            self.CC += f_floor * p_i
            return f_floor
        else:
            self.CC += f_ceil * p_i
            return f_ceil
