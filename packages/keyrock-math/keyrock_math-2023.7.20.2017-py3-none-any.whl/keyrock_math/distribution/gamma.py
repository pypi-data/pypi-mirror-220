import logging
import scipy.stats as sps
import math
from typing import Literal

from .analytic import Analytic

logger = logging.getLogger(__name__)

class Gamma(Analytic):
    t: Literal['gamma'] = 'gamma'
    a: float = 1.0
    rate: float = 1.0
    loc: float = 0.0

    def __post_init__(self):
        scale = 1.0 / self.rate
        self._rv = sps.gamma(
            a=self.a,
            loc=self.loc,
            scale=scale)

    @property
    def x_min(self):
        return 0.0

    @property
    def x_max(self):
        return math.inf
