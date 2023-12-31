from .strike import Algorithm, BoundedInstance
import numpy as np

class QThreshold(Algorithm):
    """
    We send as many people as possible home when p[i] < q * p_max
    ASSUMPTIONS FOR THEORETICAL RESULTS:
      - s[i] = n for all i
      - 1 <= p[i] <= p_max for all i
      - h[i] = 0 for all i
      - online algorithm knows the range of p[i] (important!)

    We think the optimal choice of q is q=sqrt(1/p_max)
    """
    def setup(self, q: int) -> None:
        assert isinstance(self.I, BoundedInstance)
        # TODO: Maybe add more checks here to enforce assumptions?
        # Or better, add a new instance type for this algorithm?
        self.threshold = np.floor(q * self.I.p_max)

    def decide(self, i: int, n_i: int, s_i: int, p_i: int, h_i: int) -> int:
        return min(s_i, n_i) if i == self.I.m or p_i <= self.threshold else 0
