import csv
import numpy as np
from datetime import datetime
from itertools import product, chain, repeat
from tqdm import tqdm

from algorithms.strike import *
from algorithms.FastGreedy import FastGreedy
from algorithms.Greedy import GreedyOnline
from algorithms.Qthreshold import QThreshold
from algorithms.Random import Random
from algorithms.RandomizedPmax import RandomizedPmax
from algorithms.offline import offline


ALGS: list[type[Algorithm]] = [FastGreedy, QThreshold, Random, RandomizedPmax]
N = 100
NS = [1, 2, 4, 6, 8, 10, 15, 20, 25, 30, 40, 50, 75, 100]
MS = [1, 2, 4, 6, 8, 10, 15, 20, 25, 30, 40, 50, 75, 100]
P_MAXS = np.logspace(0, 9, 20, base=2, dtype=int)


def instances(n, m, p_max, N=1000):
    for _ in range(N):
        yield BoundedInstance.random(n, m, p_max, 0)


def main():
    fname = f"{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.csv"
    with open("data.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["alg", "n", "m", "p_max", "I", "mean", "std", "min", "max"])
        vary_n = zip(NS, repeat(10), repeat(128))
        vary_m = zip(repeat(10), MS, repeat(128))
        vary_p_max = zip(repeat(10), repeat(10), P_MAXS)
        progress = tqdm(total=N*(len(NS)+len(MS)+len(P_MAXS)))
        for n, m, p_max in chain(vary_n, vary_m, vary_p_max):
            for i, I in enumerate(instances(n, m, p_max, N)):
                opt_cost = offline(I).cost
                for alg in ALGS:
                    if issubclass(alg, RandomAlgorithm):
                        if alg == RandomizedPmax:
                            solution = alg(I, 0.9, 0.1).solution(epsilon=0.01)
                        else:
                            solution = alg(I).solution()
                        alg_cost = solution.cost
                        mean = alg_cost.mean / opt_cost
                        std = alg_cost.std / opt_cost
                        min = alg_cost.min / opt_cost
                        max = alg_cost.max / opt_cost
                    elif issubclass(alg, Algorithm):
                        if alg == QThreshold:
                            solution = alg(I, np.sqrt(p_max)).solution()
                        else:
                            solution = alg(I).solution()
                        alg_cost = solution.cost
                        mean = min = max = alg_cost / opt_cost
                        std = 0
                    else:
                        raise TypeError(f"Unknown algorithm type {alg}")
                    writer.writerow([alg.name(), n, m, p_max, i, mean, std, min, max])
                progress.update()


if __name__ == "__main__":
    main()
