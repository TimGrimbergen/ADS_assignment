from online import StrikeInstance, StrikeSolution

# returns tuple ('schedule array', 'total_cost')
# terminology is the same as what's used in the paper
def solve_offline(instance: StrikeInstance) -> StrikeSolution:
    n, m = instance.n, instance.m
    s, p, h = instance.s, instance.p, instance.h

    # Total cost per day with property:
    # t[i] = p[i] + sum(h[j] for j in range(i))
    t = [p_i + sum(h[:i]) for i, p_i in enumerate(p)]

    n_i = n
    def greedy(i, s_i):
        nonlocal n_i
        f_i = min(n_i, s_i)
        n_i -= f_i
        return i, f_i, n_i

    # Sort by t[i] in ascending order.
    solution = (greedy(i, s_i) for _, i, s_i in sorted(zip(t, range(m), s)))
    # Sort by i in ascending order.
    solution = [(f_i, n_i) for _, f_i, n_i in sorted(solution)]

    # # Number of people flying on day f[i].
    # f = [0 for _ in range(m)]
    # for _, s_i, i in sorted(zip(t, s, range(m))):
    #     f[i] = min(n, s_i)
    #     n -= f[i]

    assert n == 0, "n must be 0 after all days have been scheduled"

    # # Number of people staying on day r[i], calculated by summing how many
    # # people flew home after day i.
    # r = [sum(f[i+1:]) for i in range(m)]

    return StrikeSolution(instance, solution)


if __name__ == "__main__":
    import sys

    with open(sys.argv[1]) as f:
        n = int(f.readline())
        m = int(f.readline())
        s = list(map(int, f.readline().split(sep=",")))
        p = list(map(int, f.readline().split(sep=",")))
        h = list(map(int, f.readline().split(sep=",")))

    solution, cost = solve_offline(n, m, s, p, h)
    print(f"Total cost: {cost}")
    print("Schedule:")
    for flying, staying in solution:
        print(f"  {flying:>7}, {staying:>7}")
