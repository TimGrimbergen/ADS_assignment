import numpy as np
import matplotlib.pyplot as plt
from algorithms.offline import solve_offline
from random import randint, normalvariate
from algorithms.strike import Instance, BoundedInstance, Algorithm
from typing import Iterable

# function to randomly generate test instances with certain bounds
def generate_test_instances(N=1, n=100, m=10, s=100, p=(10,100), h=(10,100), r='uniform'):
    '''
    INPUT:
        N (int)   -   number of test instances to generate
        n, m, s, p, h (int/tuple)   -   # of people, # of days, # of seats, ticket price, hotel price
        If the parameter is a tuple, e.g., p=(10,100), then for each instance we sample p according to a given randomizing strategy
        r (string)  - the randomizing strategy we want to use. Can be one of {'normal', 'uniform'}
    OUTPUT:
        instances (list[tuples])   -    a list holding N test instances
    '''
    assert r in {'normal', 'uniform'}, "r must be one of {'normal', 'uniform'}"
    n_min, n_max = (n, n) if isinstance(n, int) else (min(*n), max(*n))
    m_min, m_max = (m, m) if isinstance(m, int) else (min(*m), max(*m))
    s_min, s_max = (s, s) if isinstance(s, int) else (min(*s), max(*s))
    p_min, p_max = (p, p) if isinstance(p, int) else (min(*p), max(*p))
    h_min, h_max = (h, h) if isinstance(h, int) else (min(*h), max(*h))

    match r:
        case 'uniform':
            for _ in range(N):
                yield BoundedInstance(randint(n_min, n_max),
                       m := randint(m_min, m_max),
                       [randint(s_min, s_max) for _ in range(m)],
                       [randint(p_min, p_max) for _ in range(m)],
                       [randint(h_min, h_max) for _ in range(m)],
                       p_max, h_max)
        case 'normal':
            # Assuming the normal distribution is not skewed.
            mu_n = (n_max - n_min) / 2
            mu_m = (m_max - m_min) / 2
            mu_s = (s_max - s_min) / 2
            mu_p = (p_max - p_min) / 2
            mu_h = (h_max - h_min) / 2

            # Assuming that a normal distribution in the root form has 3 standard deviations from both sides of the mean (and is not skewed as well).
            sigma_n = (n_max - n_min) / 6
            sigma_m = (m_max - m_min) / 6
            sigma_s = (s_max - s_min) / 6
            sigma_p = (p_max - p_min) / 6
            sigma_h = (h_max - h_min) / 6

            for _ in range(N):
                yield BoundedInstance(round(normalvariate(mu_n, sigma_n)),
                       m := round(normalvariate(mu_m, sigma_m)),
                       [round(normalvariate(mu_s, sigma_s)) for _ in range(m)],
                       [round(normalvariate(mu_p, sigma_p)) for _ in range(m)],
                       [round(normalvariate(mu_h, sigma_h)) for _ in range(m)],
                       p_max, h_max)


# function that runs an online algorithm and possible tests its solution against optimal offline solution
def test_online_until_avgcase(N: int, instances: Iterable[Instance], algorithm: type[Algorithm], *args, min_iter=100, epsilon=1e-5):
    '''
    INPUT:
        instances (list[tuples])    -   a list containing (random) test instances
        online_algorithm    -   an object that takes as input (n,m) and has a function/object that
                                that can be called repeatedly in a loop
    OUTPUT:
        data (list[tuples])     -   list containing the relevant data (c-ratios and costs)
    '''

    data = np.zeros((N, 3))
    avg_ratio = 0
    for i, I in zip(range(N), instances):
        # run the online algoritm on the instance (cost is stored in 'data' variable)
        online_solution = algorithm(I, *args).solution()
        offline_solution = solve_offline(I)
        ratio = online_solution.cost / offline_solution.cost

        data[i, 0] = ratio
        data[i, 1] = online_solution.cost
        data[i, 2] = offline_solution.cost

        # fancy way to calculate the running average
        delta = (ratio - avg_ratio) / i if i > 0 else 0
        avg_ratio += delta

        if i >= min_iter and (delta := abs(delta)) < epsilon:
            print(f"Epsilon reached at iteration {i}!")
            print(f"Average is:        {avg_ratio}")
            print(f"Difference:        {delta}")
            print()
            return data[:i+1]

    return data

def plot_data(data, save_location, file_name):
    plt.figure(dpi=300)
    plt.hist(data[:,0])
    plt.title("Histogram of observed competitive ratios")
    plt.savefig(f'{save_location}/{file_name}')
