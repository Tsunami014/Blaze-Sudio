from BlazeSudio.speed import _COMPILING
if not _COMPILING:
    from . import Ix, Op, Events, Font
    from .core import Core
    from .stuff import Clock, AvgClock, Col

__all__ = [
    'Core',

    'Ix',
    'Op',
    'Events',
    'Font',

    'Clock',
    'AvgClock',
    'Col',
]

