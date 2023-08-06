from pydantic import BaseModel, Field
from typing import Union
from typing_extensions import Annotated

from keyrock_model.model import Factory

from .beta import Beta
from .constant import Constant
from .gamma import Gamma
from .logistic import Logistic
from .log_normal import LogNormal
from .normal import Normal
from .skew_normal import SkewNormal
from .uniform import Uniform
from .weibull import Weibull

Distribution = Annotated[
                Union[
                    Beta,
                    Constant,
                    Gamma,
                    Logistic,
                    LogNormal,
                    Normal,
                    SkewNormal,
                    Uniform,
                    Weibull,
                ],
                Field(discriminator='t')
            ]

factory = Factory(Distribution)
