import sys

# parent class with basic online algorithm functionality
class OnlineAlgorithms:
    
    # initialize
    def __init__(self):
        self.n_remaining = None
        self.n = None
        self.m = None
        self.decision_method = None #
        self.buffer = []

    # for some algorithms the historic data might be useful
    def append_buffer(self, instance_data):
        self.buffer.append(instance_data)

    # basically every online algorithm uses this procedure, hence it's in the parent class
    def solve_instance(self, I):
        total_price = 0 # total cost
        self.n_remaining = self.n = I[0]
        self.m = I[1]
        decisions = [[0,0] for _ in range(self.m)]
        
        for day in range(self.m):
            if self.n_remaining <= 0: # early exit
                return [decisions, total_price] 
            
            # number of seats, today
            s_day = I[2][day]

            # ticket price, today
            p_day = I[3][day]

            # hotel price, today
            h_day = I[4][day]

            # get the decision (flying, staying) from the algorithm
            flying, staying = self.decision_function(self.n_remaining, day, s_day, p_day, h_day)

            # store decisions for each day
            decisions[day] = [flying, staying]

            # update relevant variables
            self.n_remaining -= flying
            total_price += (flying * p_day) + (staying * h_day)
             
        # unsure of why this is here:
        if self.n_remaining > 0: 
            sys.exit(f"INVALID ALGORITHM! After execution of the algorithm, there are still {self.n_remaining} people remaining.")

        return [decisions, total_price]

class qThresholdOnline(OnlineAlgorithms):
    # We send as many people as possible home when p[i] < q * p_max
    # ASSUMPTIONS FOR THEORETICAL RESULTS:
    #   - s[i] = n
    #   - 1 <= p[i] <= p_max
    #   - h[i] = 0
    #   - online algorithm knows the range of p[i] (important!)

    # We think the optimal choice of q is q=sqrt(1/p_max)
    
    def __init__(self, q, p_max):
        super().__init__()
        self.threshold = q * p_max
        self.decision_function = self.get_decision_function()

    # this function instantiates the decision function
    def get_decision_function(self):

        # given some data, decide (how many people to send back, how many people to keep in a hotel)
        def decide(n_remaining, day, s_day, p_day, h_day):
            if p_day < self.threshold:
                decision = (s_day, n_remaining - s_day)
            else:
                decision = (0, n_remaining) # send no people, everyone stays 

            return decision
        
        return decide

class RandomOnline(OnlineAlgorithms):
    # base of some randomized algorithm

    def __init__(self):
        super().__init__()
        self.decision_function = self.get_decision_function()

    # this function instantiates the decision function
    def get_decision_function(self):

        # given some data, decide (how many people to send back, how many people to keep in a hotel)
        def decide(n_remaining, day, s_day, p_day, h_day):
            if "someCondition" == True:
                decision = (s_day, n_remaining - s_day) # some decision
            else:
                decision = (0, 0) # send no people, everyone stays

            return decision
        
        return decide