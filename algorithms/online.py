class OnlineAlgorithms:
    # some parent class that handles functionality that all online algorthim share

    def __init__(self):
        self.buffer = []
        self.algorithm = None 

    def instantiate_instance(self, n, m):
        self.n = n
        self.cur_n = n
        self.m = m

    # for some algorithms the historic data might be useful
    def append_buffer(self, instance_data):
        self.buffer.append(instance_data)

    # basocally every online algorithm uses this procedure, hence it's in the parent class
    def solve_instance(self, I):
        C = 0 # total cost
        n = I[0]
        m = I[1]
        
        for day in range(m):
            if self.cur_n <= 0: # early exit
                return C 
            # get the decision (f, l) from the algorithm
            f, l = self.algorithm(self.n, day, I[2][day], I[3][day], I[4][day])

            # update relevant variables
            self.cur_n -= f
            C += f * I[3][day] + l * I[4][day]
        
        if self.cur_n > 0:
            C += self.cur_n * I[3][-1]

        return C

class HastyOnline(OnlineAlgorithms):
    # example of a specific implementation of an online algorithm
    
    def __init__(self, n, m):
        super().__init__(n, m)
        self.cur_n = n
        self.algorithm = self.create_algorithm()

    # this function instantiates the online algorithm.
    def create_algorithm(self, n, m):

        # inside of the function 'create_algorithm' we create the actual function that will handle
        # the online input 
        def hasty_algorithm(cur_n, cur_m, cur_s, cur_p, cur_h):
            if cur_n > 0:
                decision = (cur_s, cur_n - cur_s)
            else:
                decision = (0, 0)

            return decision
        
        return hasty_algorithm

class qThresholdOnline(OnlineAlgorithms):
    # example of a specific implementation of an online algorithm
    # we send everyone home when p[i] < q * p_max
    # ASSUMPTIONS FOR THEORETICAL RESULTS:
    #   - s[i] = n
    #   - 1 <= p[i] <= p_max
    #   - h[i] = 0
    #   - online algorithm knows the range of p[i] (important!)
    
    def __init__(self, q, p_max):
        super().__init__()
        self.threshold = q * p_max
        self.algorithm = self.create_algorithm()

    # this function instantiates the online algorithm.
    def create_algorithm(self):

        #self.instantiate_instance(n, m) # the algorithm may need to know these parameters

        # inside of the function 'create_algorithm' we create the actual function that will handle
        # the online input 
        def qthreshold_algorithm(cur_n, cur_m, cur_s, cur_p, cur_h):
            if cur_p < self.threshold:
                decision = (cur_s, cur_n - cur_s)
            else:
                decision = (0, 0)

            return decision
        
        return qthreshold_algorithm



