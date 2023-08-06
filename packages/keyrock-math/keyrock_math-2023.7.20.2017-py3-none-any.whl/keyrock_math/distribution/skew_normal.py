import logging
import scipy.stats as sps
import math
from typing import Literal

from .analytic import Analytic

logger = logging.getLogger(__name__)

class SkewNormal(Analytic):
    t: Literal['skew_normal'] = 'skew_normal'
    loc: float = 0.0
    scale: float = 1.0
    a: float = 0.0

    def __post_init__(self):
        self._rv = sps.skewnorm(
                loc=self.loc,
                scale=self.scale,
                a=self.a
            )
