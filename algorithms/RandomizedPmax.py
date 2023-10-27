from .strike import RandomAlgorithm, BoundedInstance
import numpy as np


class RandomizedPmax(RandomAlgorithm):
    """
    Send the more people home the lower the ratio between the current seat price and the max price is
    """
    def setup(self, alpha, beta):
        assert isinstance(self.I, BoundedInstance)
        assert 0 <= alpha <= 1
        assert 0 <= beta <= 1
        self.rng = np.random.default_rng()
        self.p_max = self.I.p_max
        self.alpha = alpha # alpha \in (0,1) alpha*floor(sqrt(pmax)) will be right bound of interval
        self.beta = beta # beta \in (0,1) floor(sqrt(pmax)) + beta*(pmax - floor(sqrt(pmax))) will be right bound of interval

        p_max_round = np.floor(np.sqrt(self.p_max))
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
            return min(n_i, s_i)
        else:
            if p_i < self.a:
                probability_buy = 1
            elif self.a <= p_i < self.b:
                # probability_buy = 1/(self.a - self.b) * p_i - self.b / (self.a - self.b) # linearly decrease probability of buying tickets
                probability_buy = np.dot([p_i**2, p_i, 1], self.c) # quadratic decrease probability of buying tickets
            else: #self.b <= p_i
                probability_buy = 0
            return self.rng.binomial(n_i, probability_buy) # number tickets to buy
