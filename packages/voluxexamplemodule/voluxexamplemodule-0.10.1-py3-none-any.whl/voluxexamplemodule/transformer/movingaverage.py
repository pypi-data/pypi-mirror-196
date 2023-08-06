"""Defines the VoluxMovingAverage class."""

from typing import List

from volux import ResolveCallableParams
from volux.module import VoluxTransformer
import numpy as np

from ..util import _gen_prep_msg, _gen_cleanup_msg


class VoluxMovingAverage(VoluxTransformer):
    """An example Volux module that return a weighted moving average."""

    def __init__(self):
        """See class docstring."""
        super().__init__(
            prepare=_gen_prep_msg("VoluxMultiply"),
            cleanup=_gen_cleanup_msg("VoluxMultiply"),
        )

    @ResolveCallableParams()
    def moving_average(
        self, values: List[float], weights: List[float]
    ) -> float:
        """Return a moving average over the provided values with the provided weights."""
        return np.average(values, weights=weights)
