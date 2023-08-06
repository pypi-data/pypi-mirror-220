import logging
import scipy.stats as sps
import math
from typing import Literal

from .analytic import Analytic

logger = logging.getLogger(__name__)

class Normal(Analytic):
    t: Literal['normal'] = 'normal'
    loc: float = 0.0
    scale: float = 1.0

    def __post_init__(self):
        self._rv = sps.norm(
                self.loc,
                self.scale
            )
