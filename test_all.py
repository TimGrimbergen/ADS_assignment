import sys
import os

sys.path.insert(1, os.path.dirname(os.path.dirname(__file__))) # needed to access other code

import numpy as np
from algorithms.online import QThreshold, Random, RandomizedQThresholdOnline, RandomizedPmaxProximityOnline
from utility_functions import generate_test_instances, plot_data, test_online_until_avgcase

# use this script to automate testing multiple algorithms.

N = 100000
LAMBDA = 1 #The lambda value used as the upper limit for generating random values

p_min = 1
p_max = 100

instances = list(generate_test_instances(N=N, n=1, m=10, s=1, h=0, p=(p_min, p_max)))

data = test_online_until_avgcase(N, instances, QThreshold, np.sqrt(1/p_max))
plot_data(data, 'figures', 'qThreshold')

data = test_online_until_avgcase(N, instances, RandomizedQThresholdOnline, np.sqrt(1/p_max), LAMBDA)
plot_data(data, 'figures', 'RandomizedQThresholdOnline')

data = test_online_until_avgcase(N, instances, RandomizedPmaxProximityOnline)
plot_data(data, 'figures', 'RandomizedPmaxProximityOnline')

data = test_online_until_avgcase(N, instances, Random)
plot_data(data, 'figures', 'RandomOnline')
