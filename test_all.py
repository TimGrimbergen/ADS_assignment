import sys
import os

sys.path.insert(1, os.path.dirname(os.path.dirname(__file__))) # needed to access other code

import numpy as np
from algorithms.online import qThresholdOnline, RandomizedQThresholdOnline, RandomizedPmaxProximityOnline
from utility_functions import generate_test_instances, test_online, plot_data, test_online_until_avgcase

# use this script to automate testing multiple algorithms.

number_of_test_instances = 100000

p_min = 1
p_max = 100

instances = generate_test_instances(N=number_of_test_instances, n=100, m=20, s=100, h=50, p=(p_min, p_max))

data = test_online_until_avgcase(instances, qThresholdOnline(np.sqrt(1/p_max), p_max), number_of_test_instances / 10, 0.01)
plot_data(data, 'figures', 'qThreshold')

data = test_online_until_avgcase(instances, RandomizedQThresholdOnline(np.sqrt(1/p_max), p_max), number_of_test_instances / 10, 0.01)
plot_data(data, 'figures', 'RandomizedQThresholdOnline')

data = test_online_until_avgcase(instances, RandomizedPmaxProximityOnline(p_max), number_of_test_instances / 10, 0.01)
plot_data(data, 'figures', 'RandomizedQThresholdOnline')