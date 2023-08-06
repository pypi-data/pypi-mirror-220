import logging
import math
import numpy as np
from scipy.special import erfinv
from typing import Literal

from .analytic import Distribution

logger = logging.getLogger(__name__)

SQRT2 = math.sqrt(2)
SQRT2PI = math.sqrt(2 * math.pi)
MIN_X = 0.000000001

class LogNormal(Distribution):
    t: Literal['log_normal'] = 'log_normal'
    loc: float = 0.0
    scale: float = 1.0

    def __post_init__(self):
        self.mu = self.loc
        self.sigma = self.scale

    @property
    def x_min(self):
        return 0.0

    @property
    def x_max(self):
        return math.inf

    def pdf(self, x: float) -> float:
        # Avoid SciPy LogNormal implementation
        #  since it inteprets mu differently
        if (x < MIN_X):
            return 0.0

        PDF = 1.0 / (x * self.sigma * SQRT2PI)
        PDF *= math.exp(-1.0 * ((np.log(x) - self.mu) ** 2) / (2.0 * self.sigma * self.sigma))
        return PDF

    def cdf(self, x: float) -> float:
        # Avoid SciPy LogNormal implementation
        #  since it inteprets mu differently
        if (x < MIN_X):
            return 0.0

        CDF = 0.5 * (1.0 + math.erf((np.log(x) - self.mu) / (self.sigma * SQRT2)))
        return CDF;

    def quantile(self, p: float) -> float:
        Q = math.sqrt(2.0 * self.sigma * self.sigma)
        Q *= erfinv(2.0 * p - 1.0)
        Q += self.mu
        Q = math.exp(Q)
        return Q

    def get_random_value(self, size=1) -> float:
        if self._rng:
            return self._rng.lognormal(self.mu, self.sigma)
        else:
            return np.random.lognormal(self.mu, self.sigma)
