import sys
import os

sys.path.insert(1, os.path.dirname(os.path.dirname(__file__))) # needed to access other code

import numpy as np
from algorithms.online import QThreshold, Random, RandomizedPmaxProximityOnline, GreedyOnline, FastGreedyOnline
from utility_functions import generate_test_instances, plot_data, test_online

# use this script to automate testing multiple algorithms.

N = 100_000
LAMBDA = 1 #The lambda value used as the upper limit for generating random values

p_min = 1
p_max = 100

instances = list(generate_test_instances(N=N, n=(10), m=(10), s=1000, h=0, p=(p_min, p_max)))

qThreshold_data = test_online(N, instances, QThreshold, np.sqrt(1/p_max))
plot_data('figures', 'qThreshold', qThreshold_data)

randomizedPmaxProximityOnline_data = test_online(N, instances, RandomizedPmaxProximityOnline, 0.9, 0.2)
plot_data('figures', 'RandomizedPmaxProximityOnline', randomizedPmaxProximityOnline_data)

# random_data = test_online(N, instances, Random)
# plot_data('figures', 'RandomOnline', random_data)

# greedy_online = test_online(N, instances, GreedyOnline)
# plot_data('figures', 'GreedyOnline', greedy_online)

fast_greedy = test_online(N, instances, FastGreedyOnline)
plot_data('figures', 'FastGreedyOnline', fast_greedy)

plot_data('figures', 'violin2',
          (qThreshold_data, "qThreshold"),
          (randomizedPmaxProximityOnline_data, "Randomized\nPmaxProximity\nOnline"),
        #   (random_data, "RandomOnline"),
        #   (greedy_online, "GreedyOnline"),
          (fast_greedy, "FastGreedyOnline"))
