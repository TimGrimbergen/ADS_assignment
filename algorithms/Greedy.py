from .strike import BoundedInstance, Algorithm
import numpy as np

class GreedyOnline(Algorithm):
    def setup(self):
        assert isinstance(self.I, BoundedInstance)
        self.p_max = self.I.p_max
        self.hcumsum = [0]
        self.mineffprice = self.p_max
        self.mineffprice = self.p_max
        self.CC = 0

    def decide(self, i: int, n_i: int, s_i: int, p_i: int, h_i: int) -> int:
        if i >= self.I.m:
            return min(n_i, s_i)
        else:
            self.mineffprice = p_i + self.hcumsum[-1]
            self.hcumsum.append(self.hcumsum[-1] + h_i)
            ns = np.linspace(0, n_i, n_i+1)
            cs = np.maximum((self.CC+p_i*ns+(self.p_max+h_i)*(n_i-ns))
                            / (self.mineffprice*self.I.n),
                            (self.CC+p_i*ns+(1+h_i)*(n_i-ns))
                            / ((np.minimum(self.mineffprice,1+self.hcumsum[-1]))*self.I.n))
            f_i = np.argmin(cs) # number tickets to buy
            self.CC += f_i * p_i + (n_i - f_i) * h_i
            return f_i
