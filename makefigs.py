import csv
import matplotlib.pyplot as plt
import numpy as np


def read_and_plot(algs=[], param_vary=None):
    means = {alg : [] for alg in algs}
    stds = {alg : [] for alg in algs}
    vals = []
    n, m, pmax = None, None, None

    for file in algs:
        with open(f"data/{file}_{param_vary}.csv", newline='') as f:
            reader = csv.reader(f)
            cur_means = []
            cur_stds = []
            cur_vals = []

            i = 0
            for row in reader:
                if i == 0:
                    i+=1
                    continue
                
                if n==None or m==None or pmax == None:
                    n = int(row[0])
                    m = int(row[1])
                    pmax = int(row[2])

                if i == 1:
                    cur_ratios = []

                cur_ratios.append(float(row[4]))

                i+=1

                if i == 101: 
                    if param_vary == 'm':   
                        cur_vals.append(int(row[1]))
                    elif param_vary == 'n':
                       cur_vals.append(int(row[0]))
                    elif param_vary == 'pmax':
                         cur_vals.append(int(row[2]))

                    cur_means.append( np.mean(cur_ratios))
                    cur_stds.append(np.std(cur_ratios))
                    i = 1
            
            means[file] = cur_means
            stds[file] = cur_stds

            if len(vals) == 0:
                vals = cur_vals
            print(n,m,pmax, vals)
            print(means)

        not_varied = []
        for param in ['n', 'm', 'pmax']:
            if param != param_vary:
                val = None
                if param == 'n': val = n
                elif param == 'm': val = m
                elif param == 'pmax': val = pmax
                not_varied.append((param, val))

        plt.figure()
        for alg in algs:
            plt.plot(vals, means[alg], label=f"{alg}")
            plt.plot(vals, [means[alg][i] + stds[alg][i] for i in range(len(means[alg]))], label=f"{alg}+std")
            plt.plot(vals, [means[alg][i] - stds[alg][i] for i in range(len(means[alg]))], label=f"{alg}-std")
        plt.title(f"Fixed: ({not_varied[0][0]},{not_varied[1][0]}) = ({not_varied[0][1]},{not_varied[1][1]})")
        plt.xlabel(f"Varied: {param_vary}")
        plt.ylabel('mean competitive ratio')
        plt.xscale('log')
        plt.legend()
        plt.savefig(f"chap6figs/algs_{param_vary}.png")

read_and_plot(['Qthreshold'], 'm')
            
        