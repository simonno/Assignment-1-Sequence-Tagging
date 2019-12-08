import numpy as np

EPS = 1e-7


class MathUtils:
    @staticmethod
    def calc_fraction(counter, denominator):
        if denominator == 0:
            return EPS
        else:
            return np.divide(counter, denominator)
