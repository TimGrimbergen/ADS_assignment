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
    import sys

    with open(sys.argv[1]) as f:
        n = int(f.readline())
        m = int(f.readline())
        s = list(map(int, f.readline().split(sep=",")))
        p = list(map(int, f.readline().split(sep=",")))
        h = list(map(int, f.readline().split(sep=",")))

    solution = offline(Instance(n, m, s, p, h))
    print(f"Cost: {solution.cost}")
    print("Schedule:")
    for flying, staying in solution:
        print(f"  {flying:>7}, {staying:>7}")
