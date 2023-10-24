import sys
import random

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


LAMBDA = 1 #The lambda value used as the upper limit for generating random values
CONSIDER_N_LAST_DAYS = 3 #The number of days to consider when observing the price trend


# parent class with basic online algorithm functionality
class OnlineAlgorithms:
    
    # initialize
    def __init__(self):
        self.n_remaining = None
        self.n = None
        self.m = None
        self.decision_function = None
        self.buffer = []
        self.algorithm_name = "Unknown"

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
        
        if self.n_remaining > 0:
            sys.exit(f"INVALID ALGORITHM {self.algorithm_name}! After execution of the algorithm, there are still {self.n_remaining} people remaining, from original {self.n}. Days: {self.m}, current day: {day}")

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
        self.algorithm_name = "Q-Threshold Online"
        self.threshold = q * p_max
        self.decision_function = self.get_decision_function()

    # this function instantiates the decision function
    def get_decision_function(self):

        # given some data, decide (how many people to send back, how many people to keep in a hotel)
        def decide(n_remaining, day, s_day, p_day, h_day):
            if (day + 1) >= self.m: # if last day
                decision = (s_day, n_remaining - s_day) # send max people back
            elif p_day < self.threshold:
                decision = (s_day, n_remaining - s_day)
            else:
                decision = (0, n_remaining) # send no people, everyone stays 

            return decision
        
        return decide

class RandomOnline(OnlineAlgorithms):
    # base of some randomized algorithm

    def __init__(self):
        super().__init__()
        self.algorithm_name = "Random Online"
        self.decision_function = self.get_decision_function()

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
    
class RandomizedQThresholdOnline(RandomOnline):
    # We send n_remaining - randint(1, lambda) if enough seats are available else as many as possible when p[i] < q * p_max
    
    def __init__(self, q, p_max, lam = LAMBDA):
        super().__init__()
        self.algorithm_name = "Randomized Q-Threshold Online"
        self.threshold = q * p_max
        self.lam = lam
        self.decision_function = self.get_decision_function()

    # this function instantiates the decision function
    def get_decision_function(self):

        # given some data, decide (how many people to send back, how many people to keep in a hotel)
        def decide(n_remaining, day, s_day, p_day, h_day):
            lamI = random.randint(1, self.lam)
            if (day + 1) >= self.m: # if last day
                flying = min(n_remaining, s_day)
                staying = n_remaining - flying
                decision = (flying, staying) # send max people back
            elif p_day < self.threshold:
                flying = min(n_remaining - lamI, s_day) #Send n remaining people - random int if enough seats are available, otherwise as many as possible 
                staying = n_remaining - flying
                decision = (flying, staying)
            else:
                decision = (0, n_remaining) # send no people, everyone stays 

            return decision
        
        return decide
    

class PredictionOnline(RandomOnline):
    # We send n_remaining - randint(1, lambda) if enough seats are available else as many as possible when p[i] < q * p_max
    
    def __init__(self):
        super().__init__()
        self.algorithm_name = "Prediction Online"
        self.s_history = [] #s_history is the history of prices
        self.decision_function = self.get_decision_function()
        self.counter = 0

    def is_price_increasing(self, days):
            if len(self.s_history) < 1 or days == 0:
                return False
            x = np.array([i for i in range(len(self.s_history))]).reshape((-1, 1))
            y = np.array(self.s_history).reshape((-1, 1))
            model = LinearRegression().fit(x[:days], y[:days])
            
            return True if model.coef_ >= 0 else False
        
    def is_price_below_average(self, s_day):
        return s_day < sum(self.s_history) / len(self.s_history)
    
    # this function instantiates the decision function
    def get_decision_function(self):

        # given some data, decide (how many people to send back, how many people to keep in a hotel)
        def decide(n_remaining, day, s_day, p_day, h_day):
            self.s_history.append(s_day)
            price_increasing = self.is_price_increasing(min(day, CONSIDER_N_LAST_DAYS)) #The current price trend according to linear regression on the history of prices
            price_below_average = self.is_price_below_average(s_day)
            #Remove magic values
            probability_of_buying = (.7 if price_increasing else .3 + .8 if price_below_average else .2) / 2
            if (day + 1) >= self.m: # if last day
                flying = min(n_remaining, s_day)
                staying = n_remaining - flying
                decision = (flying, staying) # send max people back
            elif random.random() < probability_of_buying:
                flying = min(n_remaining, s_day)   
                staying = n_remaining - flying
                decision = (flying, staying)
            else:
                decision = (0, n_remaining) # send no people, everyone stays 

            return decision
        
        return decide
    
    