import sys
import math
import numpy as np
# parent class with basic online algorithm functionality
class OnlineAlgorithms:
    
    # initialize
    def __init__(self):
        self.n_remaining = None
        self.n = None
        self.m = None
        self.decision_function = None # every online algortithm needs a function that decides (f_i, l_i) for day i 
        self.buffer = []
        self.algorithm_name = "Unknown"

    # for some algorithms the historic data might be useful
    def append_buffer(self, instance_data):
        self.buffer.append(instance_data)

    # basically every online algorithm uses this procedure, hence it's in the parent class
    def solve_instance(self, I):
        self.reset()
        total_price = 0 # total cost
        self.n_remaining = self.n = I[0]
        self.m = I[1]
        decisions = [(0,0) for _ in range(self.m)]
        
        for day in range(self.m):
            if self.n_remaining <= 0: # early exit
                return decisions, total_price
            
            # number of seats, today
            s_day = I[2][day]

            # ticket price, today
            p_day = I[3][day]

            # hotel price, today
            h_day = I[4][day]

            # get the decision (flying, staying) from the algorithm
            flying, staying = self.decision_function(self.n_remaining, day, s_day, p_day, h_day)

            # store decisions for each day
            decisions[day] = (flying, staying)

            # update relevant variables
            self.n_remaining -= flying
            total_price += (flying * p_day) + (staying * h_day)
        
        if self.n_remaining > 0:
            sys.exit(f"INVALID ALGORITHM {self.algorithm_name}! After execution of the algorithm, there are still {self.n_remaining} people remaining, from original {self.n}. Days: {self.m}, current day: {day}")

        return decisions, total_price

class qThresholdOnline(OnlineAlgorithms):
    # We send as many people as possible home when p[i] < q * p_max
    # ASSUMPTIONS FOR THEORETICAL RESULTS:
    #   - s[i] = n
    #   - 1 <= p[i] <= p_max
    #   - h[i] = 0
    #   - online algorithm knows the range of p[i] (important!)

    # We think the optimal choice of q is q=sqrt(1/p_max)
    
    def __init__(self, p_max):
        super().__init__()
        self.algorithm_name = "Q-Threshold Online"
        self.threshold = math.floor(math.sqrt(p_max))
        self.decision_function = self.get_decision_function()

    def reset(self):
        pass

    # this function instantiates the decision function
    def get_decision_function(self):

        # given some data, decide (how many people to send back, how many people to keep in a hotel)
        def decide(n_remaining, day, s_day, p_day, h_day):
            if p_day <= self.threshold:
                decision = (s_day, n_remaining - s_day)
            elif (day + 1) >= self.m: # if last day
                decision = (s_day, n_remaining - s_day) # send max people back
            else:
                decision = (0, n_remaining) # send no people, everyone stays 

            return decision
        
        return decide

class RandomOnline(OnlineAlgorithms):
    # base of some randomized algorithm

    def __init__(self):
        super().__init__()
        self.algorithm_name = "Random Online"

    # this function instantiates the decision function
    def get_decision_function(self):

        # given some data, decide (how many people to send back, how many people to keep in a hotel)
        def decide(n_remaining, day, s_day, p_day, h_day):
            if "someCondition" == True: # decision function
                decision = (s_day, n_remaining - s_day)
            elif (day + 1) >= self.m: # if last day
                decision = (s_day, n_remaining - s_day) # send max people back
            else:
                decision = (0, n_remaining) # send no people, everyone stays 

            return decision
        
        return decide


class GreedyOnline(OnlineAlgorithms):
    def __init__(self, pmax):
        super().__init__()
        self.algorithm_name = "Greedy_Online" 
        self.decision_function = self.get_decision_function()
        self.pmax = pmax
        self.pmin = pmax
        self.CC = 0

    def get_decision_function(self):
        def decision(n_remaining, day, s_i, p_i, h_i):
            if day == self.m - 1: return [n_remaining, 0]
            p_min_temp = min(self.pmin, p_i)
            # x = round( (self.pmax*n_remaining - p_min_temp*n_remaining - self.CC*(p_min_temp-1) ) / ( self.pmax + p_i*p_min_temp - p_min_temp - p_i ))
            x = round( (self.pmax*n_remaining - p_i*n_remaining )/ ( self.pmax + p_i**2 - 2*p_i ))
            if x >= 1:
                self.pmin = p_min_temp
            # x = round( (self.pmax*n_remaining - self.pmin*n_remaining )/ ( self.pmax + p_i**2 - 2*p_i ))
            self.CC += x*p_i
            return [x, n_remaining - x]

        return decision
    
    def reset(self):
        self.pmin = self.pmax
        self.CC = 0
        
class SuperGreedyOnline(OnlineAlgorithms):
    def __init__(self, pmax):
        super().__init__()
        self.algorithm_name = "Super_Greedy_Online" 
        self.decision_function = self.get_decision_function()
        self.pmax = pmax
        self.pmin = pmax
        self.CC = 0

    def get_decision_function(self):
        def decision(n_remaining, day, s_i, p_i, h_i):
            if day == self.m - 1: return [n_remaining, 0]
            self.p_min = min(self.pmin, p_i)
            next_cost = [[(p_i_1, (self.CC + p_i*x + p_i_1*(n_remaining-x)) / min(self.p_min,p_i_1)) for p_i_1 in range(1,self.pmax+1)] for x in range(n_remaining+1)]
            #print(next_cost)
            next_cost_max = [(i,list(sorted(next_cost[i], key=lambda x: -x[1]))[0]) for i in range(n_remaining+1)]
            #print(next_cost_max)
            next_cost_person = list(sorted((next_cost_max), key=lambda x: x[1][1]))
            x = next_cost_person[0][0]
            #print(next_cost_person)
            self.CC += x*p_i
            return [x, n_remaining-x]

        return decision
    
    def reset(self):
        self.pmin = self.pmax
        self.CC = 0
