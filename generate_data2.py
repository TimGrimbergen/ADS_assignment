

n = 10
m = 10
pmax = [1,2,3,4,5]

def generate_data(algs, n, m, pmax):
    data = {alg : [] for alg in algs}
    means = {alg: 0 for alg in algs}

    if isinstance(n, list):
        mean_competitive_ratios = {alg : [] for alg in algs}
        for n_ in n:
            competitive_ratios_of_instance = {alg : [] for alg in algs}
            generate a large number of subinstances with m and pmax fixed
            for alg in algs:
                for subinstance in subinstances:
                    if alg is random:
                        for i in range(N):
                            compute competitive ratio of alg on the subinstance
                            if converged:
                                break
                    else:
                        compute competitive ratio of alg on the subinstance

                    append the competitive ratio to competitive_ratios_of_instance[alg]

                append mean competitive ratio of the instance to mean_competitive_ratios[alg]


