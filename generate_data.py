import csv
import numpy as np
from itertools import repeat
from tqdm import tqdm
from contextlib import ExitStack

from algorithms.strike import *
from algorithms.FastGreedy import FastGreedy
from algorithms.Greedy import GreedyOnline
from algorithms.Qthreshold import QThreshold
from algorithms.Random import Random
from algorithms.RandomizedPmax import RandomizedPmax
from algorithms.offline import offline


ALGS: list[type[Algorithm]] = [FastGreedy, QThreshold, Random, RandomizedPmax]
N = 1000
NS = [1, 2, 4, 6, 8, 10, 15, 20, 25, 30, 40, 50, 75, 100]
MS = [1, 2, 4, 6, 8, 10, 15, 20, 25, 30, 40, 50, 75, 100]
P_MAXS = np.logspace(0, 9, 20, base=2, dtype=int)


def run_algorithms(ns, ms, p_maxs, writers, total):
    with tqdm(total=N*total) as p:
        for n, m, p_max in zip(ns, ms, p_maxs):
            for i in range(N):
                I = BoundedInstance.random(n, m, p_max, 0)
                opt_cost = offline(I).cost
                for alg, writer in zip(ALGS, writers):
                    if issubclass(alg, RandomAlgorithm):
                        if alg == RandomizedPmax:
                            solution = alg(I, 0.9, 0.1).solution()
                        else:
                            solution = alg(I).solution()
                        alg_cost = solution.cost
                        mean = alg_cost.mean / opt_cost
                        std = alg_cost.std / opt_cost
                        min = alg_cost.min / opt_cost
                        max = alg_cost.max / opt_cost
                    elif issubclass(alg, Algorithm):
                        if alg == QThreshold:
                            solution = alg(I, 1/np.sqrt(p_max)).solution()
                        else:
                            solution = alg(I).solution()
                        alg_cost = solution.cost
                        mean = min = max = alg_cost / opt_cost
                        std = 0
                    else:
                        raise TypeError(f"Unknown algorithm type {alg}")
                    writer.writerow([n, m, p_max, i, mean, std, min, max])
                p.update()


def open_files(stack: ExitStack, suffix: str):
    files = [stack.enter_context(open(f"data/{alg.name()}_{suffix}.csv", "w")) for alg in ALGS]
    writers = [csv.writer(file) for file in files]
    for writer in writers:
        writer.writerow(["n", "m", "p_max", "I", "mean", "std", "min", "max"])
    return writers


def main():
    with ExitStack() as stack:
        writers = open_files(stack, "n")
        run_algorithms(NS, repeat(10), repeat(128), writers, len(NS))

    with ExitStack() as stack:
        writers = open_files(stack, "m")
        run_algorithms(repeat(10), MS, repeat(128), writers, len(MS))

    with ExitStack() as stack:
        writers = open_files(stack, "p_max")
        run_algorithms(repeat(10), repeat(10), P_MAXS, writers, len(P_MAXS))


if __name__ == "__main__":
    main()
