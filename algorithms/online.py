from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class StrikeInstance:
    n: int  # Number of people
    m: int  # Number of days
    s: list[int]  # Number of seats on day i
    p: list[int]  # Price of a seat on day i
    h: list[int]  # Hotel cost on day i

    def __post_init__(self):
        assert self.n >= 1, "n must be at least 1"
        assert self.m >= 1, "m must be at least 1"
        assert len(self.s) == len(self.p) == len(self.h) == self.m, "s, p, h must have length m"
        assert all(p_i >= 1 for p_i in self.p), "p[i] must be at least 1"
        assert all(s_i >= 1 for s_i in self.s), "s[i] must be at least 1"
        assert all(h_i >= 0 for h_i in self.h), "h[i] must be at least 0"
        assert sum(self.s) >= self.n, "sum(s) must be at least n"

    @classmethod
    def from_file(cls, file: str) -> StrikeInstance:
        with open(file, 'r') as f:
            n = int(f.readline())
            m = int(f.readline())
            s, p, h = [], [], []
            for _ in range(m):
                s_i, p_i, h_i = f.readline().split(', ')
                s.append(int(s_i))
                p.append(int(p_i))
                h.append(int(h_i))
        return cls(n, m, s, p, h)


class OnlineAlgorithm(ABC):
    @classmethod
    def __subclasshook__(cls, subclass: OnlineAlgorithm):
        return (hasattr(subclass, 'setup') and
                callable(subclass.setup) and
                hasattr(subclass, 'decide') and
                callable(subclass.decide) and
                hasattr(subclass, 'instance') or
                NotImplemented)

    def __init__(self, instance: StrikeInstance, *args, **kwargs) -> None:
        self.__instance = instance
        self.setup(*args, **kwargs)

    @property
    def instance(self) -> StrikeInstance:
        return self.__instance

    @abstractmethod
    def setup(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def decide(self, i: int, n_i: int, m_i: int, s_i: int, p_i: int, h_i: int) -> int:
        pass

    @property
    def solution(self) -> StrikeSolution:
        n, m = self.instance.n, self.instance.m
        s, p, h = self.instance.s, self.instance.p, self.instance.h
        n_i = n
        # List comprehension has better performance than initializing to zeros
        # or using append.
        def decide(i, s_i, p_i, h_i):
            nonlocal n_i
            f_i = self.decide(i, n_i, m - i, s_i, p_i, h_i)
            n_i -= f_i
            return f_i, n_i
        solution = [decide(i, s_i, p_i, h_i)
                    for i, (s_i, p_i, h_i)
                    in enumerate(zip(s, p, h))]
        return StrikeSolution(self.instance, solution)


@dataclass
class StrikeSolution:
    instance: StrikeInstance
    solution: list[tuple[int, int]]

    @property
    def cost(self) -> int:
        return sum(f_i * p_i + h_i * r_i
                   for (f_i, r_i), p_i, h_i
                   in zip(self.solution, self.instance.p, self.instance.h))


class qThresholdOnline(OnlineAlgorithm):
    __algorithm_name = "q-Threshold Online"
    # We send as many people as possible home when p[i] < q * p_max
    # ASSUMPTIONS FOR THEORETICAL RESULTS:
    #   - s[i] = n
    #   - 1 <= p[i] <= p_max
    #   - h[i] = 0
    #   - online algorithm knows the range of p[i] (important!)

    # We think the optimal choice of q is q=sqrt(1/p_max)

    def __init__(self, q, p_max):
        super().__init__()
        self.algorithm_name = "Q-Threshold Online"
        self.threshold = q * p_max
        self.decision_function = self.get_decision_function()

    # this function instantiates the decision function
    def get_decision_function(self):

        # given some data, decide (how many people to send back, how many people to keep in a hotel)
        def decide(n_remaining, day, s_day, p_day, h_day):
            if p_day < self.threshold:
                decision = (s_day, n_remaining - s_day)
            elif (day + 1) >= self.m: # if last day
                decision = (s_day, n_remaining - s_day) # send max people back
            else:
                decision = (0, n_remaining) # send no people, everyone stays

            return decision

        return decide

class RandomOnline(OnlineAlgorithm):
    # base of some randomized algorithm

    def __init__(self):
        super().__init__()
        self.algorithm_name = "Random Online"
        self.decision_function = self.get_decision_function()

    # this function instantiates the decision function
    def get_decision_function(self):

        # given some data, decide (how many people to send back, how many people to keep in a hotel)
        def decide(n_remaining, day, s_day, p_day, h_day):
            if "someCondition" == True: # decision function
                decision = (s_day, n_remaining - s_day)
            elif (day + 1) >= self.m: # if last day
                decision = (s_day, n_remaining - s_day) # send max people back
            else:
                decision = (0, n_remaining) # send no people, everyone stays

            return decision

        return decide
