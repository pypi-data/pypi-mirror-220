import logging
import scipy.stats as sps
import math
from typing import Literal

from .analytic import Analytic

logger = logging.getLogger(__name__)

class Beta(Analytic):
    t: Literal['beta'] = 'beta'
    a: float = 1.0
    b: float = 1.0

    def __post_init__(self):
        self._rv = sps.beta(
                a=self.a,
                b=self.b,
                loc=0.0,
                scale=1.0
            )

    @property
    def x_min(self):
        return 0.0

    @property
    def x_max(self):
        return 1.0
