import logging
import scipy.stats as sps
import math
from typing import Literal

from .analytic import Analytic

logger = logging.getLogger(__name__)

# Special shape values are 1 and 2
#   where Weibull distribution reduces to the expon and rayleigh distributions respectively

# The value of the scale parameter equals the 63.2 percentile in the distribution

class Weibull(Analytic):
    t: Literal['weibull'] = 'weibull'
    threshold: float = 0.0
    shape: float = 2.0 # beta or k
    scale: float = 1.0 # lambda

    def __post_init__(self):
        self._rv = sps.weibull_min(
                c=self.shape,
                loc=self.threshold,
                scale=self.scale
            )

    @property
    def x_min(self):
        return self.threshold
