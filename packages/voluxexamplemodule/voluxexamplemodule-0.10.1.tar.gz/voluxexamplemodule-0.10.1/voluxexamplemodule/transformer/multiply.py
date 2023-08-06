"""Defines the VoluxMultiply class."""

from volux import ResolveCallableParams
from volux.module import VoluxTransformer

from ..util import _gen_prep_msg, _gen_cleanup_msg


class VoluxMultiply(VoluxTransformer):
    """An example Volux module that takes values and multiplies them by the specified value."""

    def __init__(self, multiplier: float):
        """See class docstring."""
        self.multiplier = multiplier
        super().__init__(
            prepare=_gen_prep_msg("VoluxMultiply"),
            cleanup=_gen_cleanup_msg("VoluxMultiply"),
        )

    @ResolveCallableParams()
    def multiply(self, value: int) -> float:
        """Multiple specified value by multiplier set during module init."""
        return value * self.multiplier
