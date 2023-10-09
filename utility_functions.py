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
        n_ = n if isinstance(n, int) else round(random.uniform(n[0], n[1]))
        m_ = m if isinstance(m, int) else round(random.uniform(m[0], m[1]))
        s_ = [s]*m_ if isinstance(s, int) else [round(random.uniform(s[0], s[1])) for _ in range(m_)] 
        p_ = [p]*m_ if isinstance(p, int) else [round(random.uniform(p[0], p[1])) for _ in range(m_)]
        h_ = [h]*m_ if isinstance(h, int) else [round(random.uniform(h[0], h[1])) for _ in range(m_)]
        instances.append((n_, m_, s_, p_, h_))
        
    return instances

# function that runs an online algorithm and possible tests its solution against optimal offline solution
def test_online(instances, online_algorithm):
    '''
    INPUT:
        instances (list[tuples])    -   a list containing (random) test instances
        online_algorithm    -   an object that takes as input (n,m) and has a function/object that 
                                that can be called repeatedly in a loop
    OUTPUT:
        data (list[tuples])     -   list containing the relevant data (c-ratios and costs)
    '''

    data = np.zeros((len(instances),3))

    for i,I in enumerate(instances):
        # run the online algoritm on the instance (cost is stored in 'data' variable)
        online_decisions, online_total_price = online_algorithm.solve_instance(I)

        offline_decisions, offline_total_price = solve_offline(*I)

        ratio = online_total_price / offline_total_price

        data[i] = (ratio, online_total_price, offline_total_price)

    return data

# function that runs an online algorithm and possible tests its solution against optimal offline solution
def test_online_until_avgcase(instances, online_algorithm, n, change_threshold):
    '''
    INPUT:
        instances (list[tuples])    -   a list containing (random) test instances
        online_algorithm    -   an object that takes as input (n,m) and has a function/object that 
                                that can be called repeatedly in a loop
    OUTPUT:
        data (list[tuples])     -   list containing the relevant data (c-ratios and costs)
    '''

    data = np.zeros((len(instances),3))

    ratios = []
    average_ratio = 0

    for i,I in enumerate(instances):
        # run the online algoritm on the instance (cost is stored in 'data' variable)
        online_decisions, online_total_price = online_algorithm.solve_instance(I)

        offline_decisions, offline_total_price = solve_offline(*I)

        ratio = online_total_price / offline_total_price
        
        ratios.append(ratio)
        average_ratio = np.average(ratios)
                
        data[i] = (ratio, online_total_price, offline_total_price)

        if i > n:
            last_n = ratios[int(i-n):int(i)]
            last_n_average_ratio = np.average(last_n)

            if (abs(average_ratio - last_n_average_ratio) < change_threshold):
                print (f"Average is {average_ratio}, last n average is {last_n_average_ratio}, difference is {abs(average_ratio - last_n_average_ratio)}, change_threhold is {change_threshold}")
                return data

    return data

def plot_data(data, save_location, file_name):
    plt.figure(dpi=300)
    plt.hist(data[:,0])
    plt.title("Histogram of observed competitive ratios")
    plt.savefig(f'{save_location}/{file_name}')