import numpy as np

# function as defined in paper, see Lemma 1.
def total(j, p, h):
    if (j == 0):
        return p[j]
    else:
        return p[j] + np.sum(h[0:j])

# returns tuple ('schedule array', 'total_cost')
# terminology is the same as what's used in the paper
def solve_offline(n, m, s, p, h):
    total_price = [(i, s[i], total(i, p, h)) for i in range(m)]
    best_days = sorted(total_price, key = lambda x: -x[2])

    day_send = [0 for _ in range(m)]
    total_cost = 0
    n_remaining = n
    # iterate over best days, using Lemma 2 and Lemma 3.
    while n_remaining > 0:
        day, seats, price = best_days.pop()
        seats_used = max(min(n_remaining,seats), 0)
        day_send[day] = seats_used
        n_remaining -= seats_used
        total_cost += seats_used * price

    # return data conforming the requested format.
    schedule_array = [(0,0) for _ in range(m)]
    n_remaining = n
    for day,seats_used in enumerate(day_send):
        schedule_array[day] = (seats_used, n_remaining-seats_used)
        n_remaining -= seats_used

    return schedule_array, total_cost
