"""Example module."""

from typing import Callable, Any, Union, List

from volux import ResolveCallableParams
from volux.module import VoluxDestination

# package
from .source import VoluxNumber
from .transformer import VoluxMultiply
from .destination import VoluxCliBar
