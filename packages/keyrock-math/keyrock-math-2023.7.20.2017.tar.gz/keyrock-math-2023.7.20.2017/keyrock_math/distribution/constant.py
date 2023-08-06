import logging
from typing import Literal

from .analytic import Distribution

logger = logging.getLogger(__name__)

class Constant(Distribution):
    t: Literal['constant'] = 'constant'
    loc: float = 0.0

    @property
    def x_min(self):
        return self.loc

    @property
    def x_max(self):
        return self.loc

    def pdf(self, x: float) -> float:
        return self.loc

    def cdf(self, x: float) -> float:
        return self.loc * x

    def quantile(self, p: float) -> float:
        return self.loc

    def get_random_value(self, size=1) -> float:
        return self.loc
