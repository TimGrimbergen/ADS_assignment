import random
import numpy as np
import matplotlib.pyplot as plt
from algorithms.offline import solve_offline

# function to randomly generate test instances with certain bounds
def generate_test_instances(N=1, n=100, m=10, s=100, p=(10,100), h=(10,100)):
    '''
    INPUT:
        N (int)   -   number of test instances to generate
        n, m, s, p, h (int/tuple)   -   # of people, # of days, # of seats, ticket price, hotel price
        If the parameter is a tuple, e.g., p=(10,100), then for each instance we uniformly sample p
    OUTPUT:
        instances (list[tuples])   -    a list holding N test instances   
    '''

    instances = []

    for i in range(N):
        n_ = n if isinstance(n, int) else random.uniform(n[0], n[1])
        m_ = m if isinstance(m, int) else random.uniform(m[0], m[1])
        s_ = [s]*m if isinstance(s, int) else [random.uniform(s[0], s[1]) for _ in range(m)] 
        p_ = [p]*m if isinstance(p, int) else [random.uniform(p[0], p[1]) for _ in range(m)]
        h_ = [h]*m if isinstance(h, int) else [random.uniform(h[0], h[1]) for _ in range(m)]
        instances.append((n_, m_, s_, p_, h_))
        
    return instances

# function that runs an online algorithm and possible tests its solution against optimal offline solution
def test_online(instances, online_algorithm):
    '''
    INPUT:
        instances (list[tuples])    -   a list containing (random) test instances
        online_algorithm    -   a object that takes as input (n,m) and has a function/object that 
                                that can be called repeatedly in a loop
    OUTPUT:
        data (list[tuples])     -   list containing the relevant data (c-ratios and costs)
    '''

    data = np.zeros((len(instances),3))

    for i,I in enumerate(instances):
        n = I[0]
        m = I[1]

        # instantiate the online algorithm for number of people and days
        A = online_algorithm(n, m)

        # run the online algoritm on the instance (cost is stored in 'data' variable)
        data_on = A.solve_instance(I)
        data_off = solve_offline(*I)[1]

        data[i] = (data_on / data_off, data_on, data_off)
    
    return data

def plot_data(data, save_location, file_name):
    plt.figure(dpi=300)
    plt.hist(data[:,0])
    plt.title("Histogram of observed competitive ratios")
    plt.savefig(f'{save_location}/{file_name}')