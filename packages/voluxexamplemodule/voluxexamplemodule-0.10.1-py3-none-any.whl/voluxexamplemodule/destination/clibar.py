"""Defines the VoluxCliBar class."""

from typing import List

from volux import ResolveCallableParams
from volux.module import VoluxDestination

from ..util import _gen_prep_msg, _gen_cleanup_msg


class VoluxCliBar(VoluxDestination):
    """An example Volux module that takes a value and prints it as a bar to the CLI."""

    def __init__(self) -> None:
        """See class docstring."""
        super().__init__(
            prepare=_gen_prep_msg("VoluxCliBar"),
            cleanup=_gen_cleanup_msg("VoluxCliBar"),
        )

    @ResolveCallableParams()
    def print(
        self,
        segments: int,
        max_segments: int,
        level_char: str = "|",
        left_border: str = "[",
        left_fill: str = " ",
        right_fill: str = " ",
        right_border: str = "]",
    ) -> None:
        """Print a bar with x many segments."""
        print(
            f"{segments:<3} {left_border}{left_fill * (segments - 1)}{level_char if segments > 0 else ''}{right_fill * (max_segments - segments)}{right_border}"
        )

    def printPoints(
        self,
        points: List[int],
        point_chars: List[str],
        max_segments: int,
        strips: int = 0,
        strip_char: str = "|",
        left_border: str = "[",
        right_border: str = "]",
        background_char: str = " ",
    ) -> None:
        """Print a bar of a set length where points and specified chars for each point are 'plotted'."""
        # multiply the background char to fill inside of bar
        segments = [background_char for _ in range(max_segments)]
        # if strips are enabled, place down before points
        if strips > 0:
            for i in range(0, max_segments, 10):
                segments[i] = strip_char

        # for each of the points specified
        for i in range(len(points)):
            char_point = points[i]
            # if the point is outside of the maximum segment bounds or less than 0
            if i > max_segments or i < 0:
                raise ValueError(
                    "Cannot place a symbol outside of segment bounds"
                )
            # if the point is within bounds
            # overwrite char i in segments with specified character
            # TODO(Denver): check this -1 doesn't nerf highest val
            segments[max(char_point - 2, 0)] = point_chars[i]

        inner_bar = "".join(segments)

        # TODO(Denver): support multiple points in left side text
        bar = (
            f"points[0]:{points[0]:0>3} {left_border}{inner_bar}{right_border}"
        )
        print(bar)
