"""Defines the VoluxNumber class."""

from random import randrange

from volux.module import VoluxSource

from ..util import _gen_prep_msg, _gen_cleanup_msg


class VoluxNumber(VoluxSource):
    """An example Volux module that takes a minimum and maximum and returns a random number."""

    def __init__(self, _min: int, _max: int) -> None:
        """See class docstring."""
        self.min = _min
        self.max = _max
        super().__init__(
            prepare=_gen_prep_msg("VoluxNumber"),
            cleanup=_gen_cleanup_msg("VoluxNumber"),
        )

    def generate_number(self) -> int:
        """Generate a random number between the modules configured min/max."""
        return randrange(self.min, self.max)  # nosec
