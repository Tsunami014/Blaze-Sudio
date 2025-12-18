import numpy as np
from .base import OpFlags as OpFlags, TransOp as TransOp
from _typeshed import Incomplete
from typing import Iterable, overload

Number = int | float
Point = tuple[Number, Number]

class Polygon(TransOp):
    ps: Incomplete
    thickness: Incomplete
    col: Incomplete
    flags: Incomplete
    def __init__(self, ps: Iterable[Point], thickness: Number, col: np.ndarray) -> None:
        """
        Draw a closed polygon!

        Args:
            ps: The points making up the polygon
            thickness: The thickness of the line. Must be > 0.
            col: The colour of the line
        """
    def applyTrans(self, mat: np.ndarray, arr: np.ndarray) -> np.ndarray: ...

class Line(Polygon):
    @overload
    def __init__(self, p1: Point, p2: Point, thickness: Number, col: np.ndarray) -> None:
        """
        Draw a line!

        Args:
            p1: The starting point of the line (must be in format `[x, y]`)
            p2: The ending point of the line (must be in format `[x, y]`)
            thickness: The thickness of the line. Must be > 0.
            col: The colour of the line
        """
    @overload
    def __init__(self, ps: Iterable[Point], thickness: Number, col: np.ndarray) -> None:
        """
        Draw a line!

        Args:
            ps: The points of the line (must be in format `[[x1, y1], [x2, y2]]`)
            thickness: The thickness of the line. Must be > 0.
            col: The colour of the line
        """
    def applyTrans(self, mat: np.ndarray, arr: np.ndarray) -> np.ndarray: ...

class Rect(TransOp):
    @overload
    def __init__(self, pos: Point, sze: Point, thickness: Number, col: np.ndarray, /, roundness: Number = 0) -> None:
        """
        Draws a rectangle!

        Args:
            pos: The position of the rect
            sze: The size of the rect
            thickness: The thickness of the rect. If == 0, will fill the entire rect. Must be >= 0.
            col: The colour of the rect

        Keyword args:
            roundness: The roundness of the rect. 0 = ends of lines rounded, >0 = ends rounded by that many pixels, <0 = do not round the lines at all
        """
    @overload
    def __init__(self, x: Number, y: Number, width: Number, height: Number, thickness: Number, col: np.ndarray, /, roundness: Number = 0) -> None:
        """
        Draws a rectangle!

        Args:
            x: The x position of the rect
            y: The y position of the rect
            width: The width of the rect
            height: The height of the rect
            thickness: The thickness of the rect. If == 0, will fill the entire rect. Must be >= 0.
            col: The colour of the rect

        Keyword args:
            roundness: The roundness of the rect. 0 = ends of lines rounded, >0 = ends rounded by that many pixels, <0 = do not round the lines at all
        """
    def applyTrans(self, mat: np.ndarray, arr: np.ndarray) -> np.ndarray: ...

class Elipse(TransOp):
    @overload
    def __init__(self, pos: Point, xradius: Number, yradius: Number, thickness: Number, col: np.ndarray) -> None:
        """
        Draws an elipse!

        Args:
            pos: The position of the elipse
            xradius: The radius of the width of the elipse
            yradius: The radius of the height of the elipse
            thickness: The thickness of the circle. If == 0, will fill the circle entirely. Must be >= 0.
            col: The colour to fill the circle with.
        """
    @overload
    def __init__(self, x: Number, y: Number, xradius: Number, yradius: Number, thickness: Number, col: np.ndarray) -> None:
        """
        Draws an elipse! (recommended to use the other definition with `((x, y), ...)` instead of `(x, y, ...)` for readability)

        Args:
            x: The x position of the elipse
            y: The y position of the elipse
            xradius: The radius of the width of the elipse
            yradius: The radius of the height of the elipse
            thickness: The thickness of the circle. If == 0, will fill the circle entirely. Must be >= 0.
            col: The colour to fill the circle with.
        """
    def applyTrans(self, mat: np.ndarray, arr: np.ndarray) -> np.ndarray: ...

class Circle(Elipse):
    @overload
    def __init__(self, pos: Point, radius: Number, thickness: Number, col: np.ndarray) -> None:
        """
        Draws a circle!

        Args:
            pos: The position of the circle
            radius: The radius of the circle
            thickness: The thickness of the circle. If == 0, will fill the circle entirely. Must be >= 0.
            col: The colour to fill the circle with.
        """
    @overload
    def __init__(self, x: Number, y: Number, radius: Number, thickness: Number, col: np.ndarray) -> None:
        """
        Draws a circle! (recommended to use the other definition with `((x, y), ...)` instead of `(x, y, ...)` for readability)

        Args:
            x: The X position of the circle
            y: The y position of the circle
            radius: The radius of the circle
            thickness: The thickness of the circle. If == 0, will fill the circle entirely. Must be >= 0.
            col: The colour to fill the circle with.
        """
