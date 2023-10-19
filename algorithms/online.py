from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass(frozen=True)
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

    def __iter__(self) -> zip[tuple[int, int, int]]:
        return zip(self.s, self.p, self.h)


class OnlineAlgorithm(ABC):
    @classmethod
    def __subclasshook__(cls, subclass: OnlineAlgorithm):
        return (hasattr(subclass, 'setup') and
                callable(subclass.setup) and
                hasattr(subclass, 'decide') and
                callable(subclass.decide) and
                hasattr(subclass, 'instance') or
                NotImplemented)

    def __init__(self, I: StrikeInstance, *args, **kwargs) -> None:
        self.__I = I
        self.setup(*args, **kwargs)

    @property
    def I(self) -> StrikeInstance:
        return self.__I

    @abstractmethod
    def setup(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def decide(self, i: int, r_i: int, s_i: int, p_i: int, h_i: int) -> int:
        pass

    @property
    def solution(self) -> StrikeSolution:
        r_i = self.I.n
        # List comprehension has better performance than initializing to zeros
        # or using append.
        r = [r_i := r_i - self.decide(i, r_i, s_i, p_i, h_i)
             for i, (s_i, p_i, h_i) in enumerate(self.I)]
        return StrikeSolution.from_r(self.I, r)


@dataclass(frozen=True)
class StrikeSolution:
    I: StrikeInstance
    f: list[int]
    r: list[int]
    cost: int

    def __post_init__(self) -> None:
        assert len(self.f) == len(self.r) == self.I.m
        assert all(f_i >= 0 for f_i in self.f)
        assert all(r_i >= 0 for r_i in self.r)
        assert sum(self.f) == self.I.n
        assert all(n_i - f_i == r_i
                   for n_i, f_i, r_i
                   in zip(self.r, self.f[1:], self.r[1:]))
        assert self.r[-1] == 0

    @classmethod
    def no_cost(cls, I: StrikeInstance, f: list[int], r: list[int]) -> StrikeSolution:
        cost = sum(f_i * p_i + h_i * r_i for f_i, r_i, p_i, h_i in zip(f, r, I.p, I.h))
        return cls(I, f, r, cost)

    @classmethod
    def from_f(cls, I: StrikeInstance, f: list[int]) -> StrikeSolution:
        r_i = I.n
        return cls.no_cost(I, f, [r_i := r_i - f_i for f_i in f])

    @classmethod
    def from_r(cls, I: StrikeInstance, r: list[int]) -> StrikeSolution:
        print([I.n] + r[:-1], r)
        return cls.no_cost(I, [n_i - r_i for n_i, r_i in zip([I.n] + r[:-1], r)], r)

    def __iter__(self) -> zip[tuple[int, int]]:
        return zip(self.f, self.r)


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
