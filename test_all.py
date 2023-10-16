import sys
import os
import math

sys.path.insert(1, os.path.dirname(os.path.dirname(__file__))) # needed to access other code

import numpy as np
from algorithms.online import qThresholdOnline, RandomOnline, GreedyOnline, SuperGreedyOnline, DoubleThresholdOnline
from utility_functions import generate_test_instances, test_online, plot_data, test_online_until_avgcase

# use this script to automate testing multiple algorithms.

number_of_test_instances = 1000000

p_min = 1
p_max = 8
k = math.floor(math.sqrt(p_max))
print(f"p_max = {p_max} || ", k, p_max / (k+1), (p_max + k - 1) / (k+1))

instances = generate_test_instances(N=number_of_test_instances, n=10, m=5, s=10, h=(0,p_max), p=(p_min, p_max),r='uniform')
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

#data = test_online(instances, SuperGreedyOnline(p_max))
#plot_data(data, 'figures', 'qThreshold')

data = test_online(instances, DoubleThresholdOnline(p_max))
plot_data(data, 'figures', 'DoubleThreshold')