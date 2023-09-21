class OnlineAlgorithms:
    # some parent class that handles functionality that all online algorthim share

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.buffer = []

    # for some algorithms the historic data might be useful
    def append_buffer(self, instance_data):
        self.buffer.append(instance_data)

class HastyOnline(OnlineAlgorithms):
    # example of a specific implementation of an online algorithm
    
    def __init__(self, n, m):
        super().__init__(n, m)
        self.cur_n = n

        self.algorithm = self.create_algorithm()

    # this function instantiates the online algorithm.
    def create_algorithm(self):

        # inside of the function 'create_algorithm' we create the actual function that will handle
        # the online input 
        def hasty_algorithm(cur_n, cur_m, cur_s, cur_p, cur_h):
            if cur_n > 0:
                decision = (cur_s, cur_n - cur_s)
            else:
                decision = (0, 0)

            return decision
        
        return hasty_algorithm
    
    def solve_instance(self, I):
        C = 0 # total cost
        n = I[0]
        m = I[1]
        
        for day in range(m):
            # get the decision (f, l) from the algorithm
            f, l = self.algorithm(self.cur_n, day, I[2][day], I[3][day], I[4][day])

            # update relevant variables
            self.cur_n -= f
            C += f * I[3][day] + l * I[4][day]
        
        return C



