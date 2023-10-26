import sys
import os

sys.path.insert(1, os.path.dirname(os.path.dirname(__file__))) # needed to access other code

import numpy as np
from algorithms.online import QThreshold, Random, RandomizedQThresholdOnline, RandomizedPmaxProximityOnline
from utility_functions import generate_test_instances, plot_data, test_online

# use this script to automate testing multiple algorithms.

N = int(1e4)
LAMBDA = 1 #The lambda value used as the upper limit for generating random values

p_min = 1
p_max = 100

instances = list(generate_test_instances(N=N, n=1, m=10, s=1, h=0, p=(p_min, p_max)))

qThreshold_data = test_online(N, instances, QThreshold, np.sqrt(1/p_max))
plot_data('figures', 'qThreshold', qThreshold_data)

randomOnline_data = test_online(N, instances, RandomizedQThresholdOnline, np.sqrt(1/p_max), LAMBDA)
plot_data('figures', 'RandomizedQThresholdOnline', randomOnline_data)

randomizedPmaxProximityOnline_data = test_online(N, instances, RandomizedPmaxProximityOnline, 1, 0)
plot_data('figures', 'RandomizedPmaxProximityOnline', randomizedPmaxProximityOnline_data)

random_data = test_online(N, instances, Random)
plot_data('figures', 'RandomOnline', random_data)

plot_data('figures', 'violin', (qThreshold_data, "qThreshold"), (randomOnline_data, "Randomized\nQThreshold\nOnline"),
            (randomizedPmaxProximityOnline_data, "Randomized\nPmaxProximity\nOnline"), (random_data, "RandomOnline"))
