from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import chain


@dataclass(frozen=True)
class Instance:
    n: int  # Number of people
    m: int  # Number of days
    s: list[int]  # Number of seats on day i
    p: list[int]  # Price of a seat on day i
    h: list[int]  # Hotel cost on day i

    def __post_init__(self) -> None:
        assert self.n >= 1, "n must be at least 1"
        assert self.m >= 1, "m must be at least 1"
        assert len(self.s) == len(self.p) == len(self.h) == self.m, "s, p, h must have length m"
        assert all(p_i >= 1 for p_i in self.p), "p[i] must be at least 1"
        assert all(s_i >= 1 for s_i in self.s), "s[i] must be at least 1"
        assert all(h_i >= 0 for h_i in self.h), "h[i] must be at least 0"
        assert sum(self.s) >= self.n, "sum(s) must be at least n"

    @classmethod
    def from_file(cls, file: str) -> Instance:
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


@dataclass(frozen=True)
class BoundedInstance(Instance):
    p_max: int
    h_max: int

    def __post_init__(self) -> None:
        super().__post_init__()
        assert self.p_max >= 1, "p_max must be at least 1"
        assert self.h_max >= 0, "h_max must be at least 0"
        assert all(p_i <= self.p_max for p_i in self.p), "p[i] must be at most p_max"
        assert all(h_i <= self.h_max for h_i in self.h), "h[i] must be at most h_max"


@dataclass(frozen=True)
class Solution:
    I: Instance
    f: list[int]
    r: list[int]
    cost: int

    def __post_init__(self) -> None:
        assert len(self.f) == len(self.r) == self.I.m, "f and r must have length m"
        assert all(f_i >= 0 for f_i in self.f), "f[i] must be at least 0"
        assert all(r_i >= 0 for r_i in self.r), "r[i] must be at least 0"
        assert sum(self.f) == self.I.n, "sum(f) must be n"
        assert all(f_i + r_i == n_i for n_i, f_i, r_i
                   in zip(chain([self.I.n], self.r), self.f, self.r)), \
            "f[i] + r[i] must be n[i]"
        assert self.r[-1] == 0, "r[m-1] must be 0"

    @classmethod
    def no_cost(cls, I: Instance, f: list[int], r: list[int]) -> Solution:
        cost = sum(f_i * p_i + h_i * r_i for f_i, r_i, p_i, h_i in zip(f, r, I.p, I.h))
        return cls(I, f, r, cost)

    @classmethod
    def from_f(cls, I: Instance, f: list[int]) -> Solution:
        n_i = I.n
        return cls.no_cost(I, f, [n_i := n_i - f_i for f_i in f])

    @classmethod
    def from_r(cls, I: Instance, r: list[int]) -> Solution:
        return cls.no_cost(I, [n_i - r_i for n_i, r_i in zip(chain([I.n], r), r)], r)

    def __iter__(self) -> zip[tuple[int, int]]:
        return zip(self.f, self.r)


class Algorithm(ABC):
    @classmethod
    def __subclasshook__(cls, subclass: Algorithm):
        return (hasattr(subclass, 'setup') and
                callable(subclass.setup) and
                hasattr(subclass, 'decide') and
                callable(subclass.decide) and
                hasattr(subclass, 'instance') or
                NotImplemented)

    def __init__(self, I: Instance, *args, **kwargs) -> None:
        self.__I = I
        self.setup(*args, **kwargs)

    @property
    def I(self) -> Instance:
        return self.__I

    @abstractmethod
    def setup(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def decide(self, i: int, r_i: int, s_i: int, p_i: int, h_i: int) -> int:
        pass

    @property
    def solution(self) -> Solution:
        r_i = self.I.n
        # List comprehension has better performance than initializing to zeros
        # or using append.
        r = [r_i := r_i - self.decide(i, r_i, s_i, p_i, h_i)
             for i, (s_i, p_i, h_i) in enumerate(self.I, start=1)]
        return Solution.from_r(self.I, r)
