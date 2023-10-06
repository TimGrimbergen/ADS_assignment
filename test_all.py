import sys
import os

sys.path.insert(1, os.path.dirname(os.path.dirname(__file__))) # needed to access other code

import numpy as np
from algorithms.online import qThresholdOnline, RandomOnline
from utility_functions import generate_test_instances, test_online, plot_data

# use this script to automate testing multiple algorithms.

number_of_test_instances = 1000

p_min = 1
p_max = 100

instances = generate_test_instances(N=number_of_test_instances, n=1, m=10, s=1, h=0, p=(p_min, p_max))

data = test_online(instances, qThresholdOnline(np.sqrt(1/p_max), p_max))
plot_data(data, 'figures', 'qThreshold')

data = test_online(instances, RandomOnline())
plot_data(data, 'figures', 'RandomOnline')