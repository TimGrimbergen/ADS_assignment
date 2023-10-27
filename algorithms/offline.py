import sys
from .strike import Instance, Solution
from itertools import accumulate, chain


def offline(I: Instance) -> Solution:
    n_i = I.n
    h_tot = chain([0], accumulate(I.h))
    t = [p_i + h_tot_i for p_i, h_tot_i in zip(I.p, h_tot)]
    f = sorted((i, (f_i := min(n_i, s_i)), n_i := n_i - f_i)
               for _, i, s_i in sorted(zip(t, range(I.m), I.s)))
    return Solution.from_f(I, [f_i for _, f_i, _ in f])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 offline.py <instance>")
        sys.exit(1)
    I = Instance.from_file(sys.argv[1])
    solution = offline(I)
    for flying, staying in solution:
        print(f"({flying:>7}, {staying:>7})")
