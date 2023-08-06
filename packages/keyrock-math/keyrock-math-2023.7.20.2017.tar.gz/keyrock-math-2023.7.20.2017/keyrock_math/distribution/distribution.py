import logging
import numpy as np
import scipy.stats as sps
import math
from typing import List, Literal

from abc import abstractmethod
from keyrock_model.model import KrBaseModel

logger = logging.getLogger(__name__)

class Distribution(KrBaseModel):
    t: Literal['base'] = 'base'
    _x_space: None = None
    _rng: None = None

    @property
    def x_min(self):
        return -math.inf

    @property
    def x_max(self):
        return math.inf

    @abstractmethod
    def pdf(self, x: float) -> float:
        raise NotImplementedError()

    @abstractmethod
    def cdf(self, x: float) -> float:
        raise NotImplementedError()

    @abstractmethod
    def quantile(self, p: float) -> float:
        raise NotImplementedError()

    def get_random_value(self, size=1) -> float:
        raise NotImplementedError()

    def set_rng(self, rng):
        self._rng = rng

    ### Helpers ###

    def get_percentile(self, p):
        return self.quantile(p)

    def get_x_space(self):
        if self._x_space is None:
            self._x_space = np.linspace(self.quantile(0.01), self.quantile(0.99), 100)
        return self._x_space
