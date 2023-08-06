import logging
import scipy.stats as sps
import math
from typing import Literal

from .analytic import Analytic

logger = logging.getLogger(__name__)

class Uniform(Analytic):
    t: Literal['uniform'] = 'uniform'
    a: float = 0.0
    b: float = 1.0

    def __post_init__(self):
        scale = self.b - self.a
        self._rv = sps.uniform(
                loc=self.a,
                scale=scale
            )

    @property
    def x_min(self):
        return self.a

    @property
    def x_max(self):
        return self.b
