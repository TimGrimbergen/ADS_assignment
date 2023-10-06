import random
import numpy as np
import matplotlib.pyplot as plt
from algorithms.offline import solve_offline

# function to randomly generate test instances with certain bounds
def generate_test_instances(N=1, n=100, m=10, s=100, p=(10,100), h=(10,100), r='uniform'):
    '''
    INPUT:
        N (int)   -   number of test instances to generate
        n, m, s, p, h (int/tuple)   -   # of people, # of days, # of seats, ticket price, hotel price
        If the parameter is a tuple, e.g., p=(10,100), then for each instance we sample p according to a given randomizing strategy
        r (string)  - the randomizing strategy we want to use. Can be one of {'normal', 'uniform'}
    OUTPUT:
        instances (list[tuples])   -    a list holding N test instances   
    '''

    instances = []
    match r:
        case 'uniform':
            for i in range(N):
                n_ = n if isinstance(n, int) else round(random.uniform(n[0], n[1]))
                m_ = m if isinstance(m, int) else round(random.uniform(m[0], m[1]))
                s_ = [s]*m_ if isinstance(s, int) else [round(random.uniform(s[0], s[1])) for _ in range(m_)] 
                p_ = [p]*m_ if isinstance(p, int) else [round(random.uniform(p[0], p[1])) for _ in range(m_)]
                h_ = [h]*m_ if isinstance(h, int) else [round(random.uniform(h[0], h[1])) for _ in range(m_)]
                instances.append((n_, m_, s_, p_, h_))
        case 'normal':
            # Assuming the normal distribution is not skewed.
            mu_n = 0 if isinstance(n, int) else (n[1] - n[0]) / 2
            mu_m = 0 if isinstance(m, int) else (m[1] - m[0]) / 2
            mu_s = 0 if isinstance(s, int) else (s[1] - s[0]) / 2
            mu_p = 0 if isinstance(p, int) else (p[1] - p[0]) / 2
            mu_h = 0 if isinstance(h, int) else (h[1] - h[0]) / 2
            print(mu_n, mu_m, mu_s, mu_p, mu_h)

            # Assuming that a normal distribution in the root form has 3 standard deviations from both sides of the mean (and is not skewed as well).
            sigma_n = 0 if isinstance(n, int) else (n[1] - n[0]) / 6
            sigma_m = 0 if isinstance(m, int) else (m[1] - m[0]) / 6
            sigma_s = 0 if isinstance(s, int) else (s[1] - s[0]) / 6
            sigma_p = 0 if isinstance(p, int) else (p[1] - p[0]) / 6
            sigma_h = 0 if isinstance(h, int) else (h[1] - h[0]) / 6
            print(sigma_n, sigma_m, sigma_s, sigma_p, sigma_h)

            for i in range(N):
                n_ = n if isinstance(n, int) else round(random.normalvariate(mu_n, sigma_n))
                m_ = m if isinstance(m, int) else round(random.normalvariate(mu_m, sigma_m))
                s_ = [s]*m_ if isinstance(s, int) else [round(random.normalvariate(mu_s, sigma_s)) for _ in range(m_)] 
                p_ = [p]*m_ if isinstance(p, int) else [round(random.normalvariate(mu_p, sigma_p)) for _ in range(m_)]
                h_ = [h]*m_ if isinstance(h, int) else [round(random.normalvariate(mu_h, sigma_h)) for _ in range(m_)]
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

        data[i] = (online_total_price / offline_total_price, online_total_price, offline_total_price)
    
    return data

def plot_data(data, save_location, file_name):
    plt.figure(dpi=300)
    plt.hist(data[:,0])
    plt.title("Histogram of observed competitive ratios")
    plt.savefig(f'{save_location}/{file_name}')

instances = generate_test_instances(m=30, r='normal')
print(instances)
