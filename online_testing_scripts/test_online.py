import sys
import os

sys.path.insert(1, os.path.dirname(os.path.dirname(__file__))) # needed to access other code

import numpy as np
from algorithms.online import qThresholdOnline
from utility_functions import generate_test_instances, test_online, plot_data

N = 100

p_min = 1
p_max = 10

instances = generate_test_instances(N=N, n=1, m=10, s=1, h=0, p=(p_min, p_max))

data = test_online(instances, qThresholdOnline(0.3, p_max))

plot_data(data, '../figures', 'qThreshold')