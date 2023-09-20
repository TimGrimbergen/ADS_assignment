import random

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
        s_ = s if isinstance(s, int) else random.uniform(s[0], s[1])
        p_ = p if isinstance(p, int) else random.uniform(p[0], p[1])
        h_ = h if isinstance(h, int) else random.uniform(h[0], h[1])
        instances.append((n_, m_, s_, p_, h_))
        
    return instances

# function that runs an online algorithm and possible tests its solution against optimal offline solution
def test_online(instances, online_algorithm, offline_algorithm=None):
    '''
    INPUT:
        instances (list[tuples])    -   a list containing (random) test instances
        online_algorithm    -   a object that takes as input (n,m) and has a function/object that 
                                that can be called repeatedly in a loop
    '''