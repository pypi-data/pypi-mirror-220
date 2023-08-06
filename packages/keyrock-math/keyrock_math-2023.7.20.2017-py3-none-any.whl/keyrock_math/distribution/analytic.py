import logging
import numpy as np
import scipy.stats as sps
import math
from typing import List, Literal

from abc import abstractmethod

from .distribution import Distribution

logger = logging.getLogger(__name__)

cache_size = 100

class Analytic(Distribution):
    _rv: None = None
    _rv_cache: None = None
    _rv_index: int = 0

    def pdf(self, x:float) -> float:
        return self._rv.pdf(x)

    def cdf(self, x:float) -> float:
        return self._rv.cdf(x)

    def quantile(self, p:float) -> float:
        return self._rv.ppf(p)

    def get_random_value(self, size=1) -> float:
        # Build a new cache when limit is reached
        if self._rv_cache is None or self._rv_index >= cache_size:
            self._rv_index = 0
            self._rv_cache = self._rv.rvs(cache_size, random_state=self._rng)

        val = self._rv_cache[self._rv_index]
        self._rv_index += 1

        return val
