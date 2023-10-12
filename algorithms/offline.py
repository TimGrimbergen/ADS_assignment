# returns tuple ('schedule array', 'total_cost')
# terminology is the same as what's used in the paper
def solve_offline(n: int, m: int, s: list[int], p: list[int], h: list[int]):
    assert n >= 1, "n must be at least 1"
    assert m >= 1, "m must be at least 1"
    assert len(s) == len(p) == len(h) == m, "s, p, h must have length m"
    assert all(p_i >= 1 for p_i in p), "p[i] must be at least 1"
    assert all(s_i >= 1 for s_i in s), "s[i] must be at least 1"
    assert all(h_i >= 0 for h_i in h), "h[i] must be at least 0"
    assert sum(s) >= n, "sum(s) must be at least n"

    # Total cost per day with property:
    # t[i] = p[i] + sum(h[j] for j in range(i))
    t = [p_i + sum(h[:i]) for i, p_i in enumerate(p)]

    # Number of people flying on day f[i].
    f = [0 for _ in range(m)]
    for _, s_i, i in sorted(zip(t, s, range(m))):
        f[i] = min(n, s_i)
        n -= f[i]

    assert n == 0, "n must be 0 after all days have been scheduled"

    # Number of people staying on day r[i], calculated by summing how many
    # people flew home after day i.
    r = [sum(f[i+1:]) for i in range(m)]

    # Format to: (flying, staying), total_cost
    return list(zip(f, r)), sum(f[i] * t[i] for i in range(m))


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
