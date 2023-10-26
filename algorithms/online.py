import math
import random
from .strike import BoundedInstance, Algorithm, RandomAlgorithm


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


class Random(RandomAlgorithm):
    """
    Basic randomized algoithm, aka the "haha randint go brrrrr"-algorithm.
    """

    def setup(self) -> None:
        assert isinstance(self.I, BoundedInstance)
        # TODO: Maybe add an optional seed here?

    def decide(self, i: int, n_i: int, s_i: int, p_i: int, h_i: int) -> int:
        return random.randint(0, min(s_i, n_i)) if i < self.I.m else min(s_i, n_i)

class RandomizedQThresholdOnline(RandomAlgorithm):
    # We send n_i - randint(1, lambda) if enough seats are available else as many as possible when p[i] < q * p_max

    def setup(self, q: int, lam: int):
        self.threshold = q * self.I.p_max
        self.lam = lam

    # given some data, decide (how many people to send back, how many people to keep in a hotel)
    def decide(self, i: int, n_i: int, s_i: int, p_i: int, h_i: int) -> int:
        lamI = random.randint(1, self.lam)
        if (i + 1) >= self.I.m: # if last day
            flying = min(n_i, s_i)
            decision = flying # send max people back
        elif p_i < self.threshold:
            flying = min(n_i - lamI, s_i) #Send n remaining people - random int if enough seats are available, otherwise as many as possible
            decision = flying
        else:
            decision = 0 # send no people, everyone stays

        return decision


class RandomizedPmaxProximityOnline(RandomAlgorithm):
    # Send the more people home the lower the ratio between the current seat price and the max price is

    def setup(self, alpha, beta):
        self.p_max = self.I.p_max
        self.alpha = alpha # alpha \in (0,1) alpha*floor(sqrt(pmax)) will be right bound of interval
        self.beta = beta # beta \in (0,1) floor(sqrt(pmax)) + beta*(pmax - floor(sqrt(pmax))) will be right bound of interval

        p_max_round = math.floor(math.sqrt(self.p_max))
        self.a = alpha * p_max_round
        self.b = p_max_round + beta*(self.p_max - p_max_round)

    # given some data, decide (how many people to send back, how many people to keep in a hotel)
    def decide(self, i: int, n_i: int, s_i: int, p_i: int, h_i: int) -> int:
        alpha, beta = math.floor(math.sqrt(self.p_max)), math.floor(math.sqrt(self.p_max))
        if (i + 1) >= self.I.m: # if last day
            flying = min(n_i, s_i)
            decision = flying # send max people back
        else:
            if p_i < self.a:
                probability_buy = 1
            elif self.a <= p_i < self.b:
                probability_buy = 1/(self.a - self.b) * p_i - self.b / (self.a - self.b) # linearly decrease probability of buying tickets
            else: #self.b <= p_i
                probability_buy = 0
            flying = sum([random.random() < probability_buy for i in range(n_i)])
            decision = flying
        return decision
