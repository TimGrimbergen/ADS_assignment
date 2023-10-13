import sys
import os

sys.path.insert(1, os.path.dirname(os.path.dirname(__file__))) # needed to access other code

import numpy as np
from algorithms.online import qThresholdOnline, RandomOnline, GreedyOnline, SuperGreedyOnline
from utility_functions import generate_test_instances, test_online, plot_data, test_online_until_avgcase

# use this script to automate testing multiple algorithms.

number_of_test_instances = 1000

p_min = 1
p_max = 25

instances = generate_test_instances(N=number_of_test_instances, n=20, m=5, s=20, h=0, p=(p_min, p_max))
'''
data = test_online_until_avgcase(instances, qThresholdOnline(np.sqrt(1/p_max), p_max), number_of_test_instances / 10, 0.01)
plot_data(data, 'figures', 'qThreshold')

data = test_online_until_avgcase(instances, RandomOnline(), number_of_test_instances / 10, 0.01)
plot_data(data, 'figures', 'RandomOnline')
'''

#data = test_online(instances, GreedyOnline(pmax=p_max))
#plot_data(data, 'figures', 'GreedyOnline')

#data = test_online(instances, qThresholdOnline(p_max))
#plot_data(data, 'figures', 'qThreshold')

data = test_online(instances, SuperGreedyOnline(p_max))
plot_data(data, 'figures', 'qThreshold')