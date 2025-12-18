from . import Draw as Draw, Events as Events, Ix as Ix, Op as Op
from .surf import Surface as Surface, Window as Window
from _typeshed import Incomplete
from typing import overload

__all__ = ['Draw', 'Ix', 'Op', 'Events', 'Window', 'Surface', 'Clock', 'AvgClock', 'Col']

class Clock:
    dt: int
    def __init__(self) -> None: ...
    def tick(self, maxfps: int | float = None):
        """
        Ticks the clock, updating FPS count and optionally enforcing a maximum FPS.

        Args:
            maxfps: The maximum fps the application should run at. Defaults to None (don't enforce)
        """
    def get_fps(self):
        """
        Returns the number of frames per second instantly
        """

class AvgClock(Clock):
    secs: Incomplete
    goodEnough: bool
    def __init__(self, secs: int | float = 5) -> None:
        """
        An average Clock, averaging the fps over a set time.

        Args:
            secs: The number of seconds to average the fps over. Defaults to 5
        """
    def tick(self, maxfps: int | float = None):
        """
        Ticks the clock, updating FPS count and optionally enforcing a maximum FPS.

        Args:
            maxfps: The maximum fps the application should run at. Defaults to None (don't enforce)
        """
    def get_fps(self):
        """
        Returns the average FPS over the last secs seconds.
        """
    def get_fps_inst(self):
        """
        Returns the number of frames per second instantly
        """
colourType = tuple[int, int, int, int]

class Col:
    """
    A Colour is an rgb tuple.
    
    This class gives some helper functions for creating these tuples based off of different colour types.
    """
    @overload
    def __new__(cls, hex: str): ...
    @overload
    def __new__(cls, r: int, g: int, b: int, a: int = 255): ...
    @classmethod
    def rgb(cls, r: int, g: int, b: int, a: int = 255) -> colourType: ...
    @classmethod
    def rgba(cls, r: int, g: int, b: int, a: int) -> colourType: ...
    @classmethod
    def hex(cls, hex: str) -> colourType: ...
    @classmethod
    def to_rgb(cls, col: colourType) -> tuple[int, int, int]: ...
    @classmethod
    def to_rgba(cls, col: colourType) -> tuple[int, int, int, int]: ...
    @classmethod
    def to_hex(cls, col: colourType, upper: bool = True) -> str: ...
    Black: Incomplete
    Grey: Incomplete
    White: Incomplete
    Transparent: Incomplete
