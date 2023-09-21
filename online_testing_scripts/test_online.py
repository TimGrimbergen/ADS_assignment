import sys
import os

sys.path.insert(1, os.path.dirname(os.path.dirname(__file__))) # needed to access other code

from algorithms.online import HastyOnline
from utility_functions import generate_test_instances, test_online, plot_data

N = 1000

instances = generate_test_instances(N=N, h=(1,5))

data = test_online(instances, HastyOnline)

plot_data(data, '../figures', 'try2')