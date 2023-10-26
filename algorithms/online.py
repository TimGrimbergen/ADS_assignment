import sys
import random
import numpy as np
import math
from .strike import BoundedInstance, Algorithm


class QThreshold(Algorithm):
    """
    We send as many people as possible home when p[i] < q * p_max
    ASSUMPTIONS FOR THEORETICAL RESULTS:
      - s[i] = n for all i
      - 1 <= p[i] <= p_max for all i
      - h[i] = 0 for all i
      - online algorithm knows the range of p[i] (important!)

    We think the optimal choice of q is q=sqrt(1/p_max)
    """

    def setup(self, q: int) -> None:

        assert isinstance(self.I, BoundedInstance)
        # TODO: Maybe add more checks here to enforce assumptions?
        # Or better, add a new instance type for this algorithm?
        self.threshold = math.floor(q * self.I.p_max)

    def decide(self, i: int, n_i: int, s_i: int, p_i: int, h_i: int) -> int:
        return min(s_i, n_i) if i == self.I.m or p_i <= self.threshold else 0


class Random(Algorithm):
    """
    Basic randomized algoithm, aka the "haha randint go brrrrr"-algorithm.
    """

    def setup(self) -> None:
        assert isinstance(self.I, BoundedInstance)
        self.decisions = [0] * self.I.m
        for _ in range(self.I.n):
            self.decisions[random.randint(0, self.I.m - 1)] += 1


    def decide(self, i: int, n_i: int, s_i: int, p_i: int, h_i: int) -> int:
        return self.decisions[i-1]


class RandomizedPmaxProximityOnline(Algorithm):
    # Send the more people home the lower the ratio between the current seat price and the max price is

    def setup(self, alpha, beta):
        self.p_max = self.I.p_max
        self.alpha = alpha # alpha \in (0,1) alpha*floor(sqrt(pmax)) will be right bound of interval
        self.beta = beta # beta \in (0,1) floor(sqrt(pmax)) + beta*(pmax - floor(sqrt(pmax))) will be right bound of interval

        p_max_round = math.floor(np.sqrt(self.p_max))
        self.a = (a := alpha * p_max_round)
        self.b = (b := p_max_round + beta*(self.p_max - p_max_round))

        A = np.array([[      a**2,       a, 1],
                      [(a+b**2)/4, (a+b)/2, 1],
                      [      b**2,       b, 1]])
        V = np.array([1, 0.25, 0])
        self.c = np.linalg.inv(A) @ V


    # given some data, decide (how many people to send back, how many people to keep in a hotel)
    def decide(self, i: int, n_i: int, s_i: int, p_i: int, h_i: int) -> int:
        if i == self.I.m: # if last day
            flying = min(n_i, s_i)
            decision = flying # send max people back
        else:
            if p_i < self.a:
                probability_buy = 1
            elif self.a <= p_i < self.b:
                # probability_buy = 1/(self.a - self.b) * p_i - self.b / (self.a - self.b) # linearly decrease probability of buying tickets
                probability_buy = np.dot([p_i**2, p_i, 1], self.c) # quadratic decrease probability of buying tickets
            else: #self.b <= p_i
                probability_buy = 0
            flying = sum([random.random() < probability_buy for _ in range(n_i)])
            decision = flying
        return decision


class GreedyOnline(Algorithm):
    def setup(self):
        self.p_max = self.I.p_max
        self.hcumsum = [0]
        self.mineffprice = self.p_max
        self.mineffprice = self.p_max
        self.CC = 0

    def decide(self, i: int, n_i: int, s_i: int, p_i: int, h_i: int) -> int:
        if i >= self.I.m:
            flying = min(n_i, s_i)
            decision = flying
        else:

            self.mineffprice = p_i + self.hcumsum[-1]
            self.hcumsum.append(self.hcumsum[-1] + h_i)
            c = []
            # could store known values and binary search...
            for j in range(0, n_i+1):
                c.append(max( (self.CC+p_i*j+(self.p_max+h_i)*(n_i-j)) / (self.mineffprice*self.I.n),
                                (self.CC+p_i*j+(1+h_i)*(n_i-j)) / ((min(self.mineffprice,1+self.hcumsum[-1]))*self.I.n)))
            #print(p_i, n_remaining, self.CC, self.pmin, c)
            flying = np.argmin(c) # number tickets to buy
            decision = flying

            self.CC += flying*p_i + (n_i-flying) * h_i

        return decision


class FastGreedyOnline(Algorithm):
    def setup(self):
        assert isinstance(self.I, BoundedInstance)
        self.p_min = self.I.p_max
        self.CC = 0

    def decide(self, i: int, n_i: int, s_i: int, p_i: int, h_i: int) -> int:
        if i == self.I.m:
            return min(n_i, s_i)
        self.p_min = min(self.p_min, p_i)
        f_estimate = (((self.I.p_max - self.p_min) * n_i - self.CC * (self.p_min - 1)) /
                      (self.I.p_max + p_i * self.p_min - p_i - self.p_min))
        f_estimate = max(f_estimate, 0)
        worst_cost = lambda f_i: \
            max((self.CC + p_i * f_i + self.I.p_max * (n_i - f_i)) / (self.p_min * self.I.n),
                (self.CC + p_i * f_i + n_i - f_i) / self.I.n)
        # print(f"p_min = {self.p_min}")
        # print(f"CC = {self.CC}")
        # print(f"f_est = {f_estimate}")
        # print()
        if worst_cost(f_floor := math.floor(f_estimate)) < worst_cost(f_ceil := math.ceil(f_estimate)):
            self.CC += f_floor * p_i
            return f_floor
        else:
            self.CC += f_ceil * p_i
            return f_ceil
