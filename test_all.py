import sys
import os

sys.path.insert(1, os.path.dirname(os.path.dirname(__file__))) # needed to access other code

import numpy as np
from algorithms.online import QThreshold, Random
from utility_functions import generate_test_instances, plot_data, test_online_until_converged

# use this script to automate testing multiple algorithms.

N = 100000

p_min = 1
p_max = 100

instances = list(generate_test_instances(N=N, n=1, m=10, s=1, h=0, p=(p_min, p_max)))

qThreshold_data = test_online_until_converged(N, instances, QThreshold, 1/np.sqrt(p_max))
plot_data('figures', 'qThreshold', qThreshold_data)

RandomOnline_data = test_online_until_converged(N, instances, Random)
plot_data('figures', 'RandomOnline', RandomOnline_data)

plot_data('figures', 'violin', qThreshold_data, RandomOnline_data)
