from abc import ABC, abstractmethod
from typing import Iterator, Iterable


class StrikeInstance:
    def __init__(self, n: int, m: int, s: Iterable[int],
                 p: Iterable[int], h: Iterable[int]) -> None:
        """
        Inputs:
            n: number of people
            m: number of days
            s: number of seats available on each day
            p: plane ticket price on each day
            h: hotel price on each day
        """
        assert n > 0, "n must be positive"
        assert m > 0, "m must be positive"
        assert len(s) == len(p) == len(h) == m, "s, p, h must have length m"
        self.__n = n; self.__m = m
        self.__s = tuple(s)
        self.__p = tuple(p)
        self.__h = tuple(h)

    @property
    def n(self) -> int:
        return self.__n

    @property
    def m(self) -> int:
        return self.__m

    @property
    def s(self) -> list[int]:
        return list(self.__s)

    @property
    def p(self) -> list[int]:
        return list(self.__p)

    @property
    def h(self) -> list[int]:
        return list(self.__h)

    def __len__(self) -> int:
        return self.m

    def __iter__(self) -> Iterator[tuple[int, int, int]]:
        for i in range(self.m):
            yield self.__s[i], self.__p[i], self.__h[i]


class OnlineAlgorithm(ABC):
    __algorithm_name = "Online Algorithm"

    @property
    def algorithm_name(self) -> str:
        return self.__algorithm_name

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'setup') and
                callable(subclass.setup) and
                hasattr(subclass, 'decide') and
                callable(subclass.decide) or
                NotImplemented)

    def __init__(self, instance: StrikeInstance) -> None:
        self.__instance = instance
        self.__cost = 0
        self.__i = 0
        self.__f = []
        self.__r = []

    @property
    def instance(self) -> StrikeInstance:
        return self.__instance

    @property
    def cost(self) -> int:
        if self.__i < self.instance.m:
            self.run()
        return self.__cost

    @property
    def f(self) -> list[int]:
        if self.__i < self.instance.m:
            self.run()
        return self.__f

    @property
    def r(self) -> list[int]:
        if self.__i < self.instance.m:
            self.run()
        return self.__r

    def __iter__(self) -> Iterator[tuple[int, int]]:
        for i, (s_i, p_i, h_i) in enumerate(self.instance):
            if i < self.__i:  # already decided
                yield self.__f[i], self.__r[i]
            else:  # decide if not already decided
                n_i = self.instance.n if i == 0 else self.__r[i - 1]
                f_i = self.decide(i, n_i, s_i, p_i, h_i)
                r_i = n_i - f_i
                self.__f.append(f_i)
                self.__r.append(r_i)
                self.__cost += f_i * p_i + r_i * h_i
                self.__i += 1
                yield f_i, r_i

    def run(self) -> None:
        for _ in self:
            pass

    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def decide(self, i: int, n_i: int, s_i: int, p_i: int, h_i: int) -> int:
        pass


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
