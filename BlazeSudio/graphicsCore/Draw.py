from typing import overload, Iterable, Tuple
from .base import OpFlags, TransOp
from ._calcs import _drawThickLine, _drawRect, _drawCirc, _drawElipse
import numpy as np
import math

Number = int|float
Point = Tuple[Number, Number]

class Polygon(TransOp):
    __slots__ = ['ps', 'thickness', 'col', 'round']
    def __init__(self, ps: Iterable[Point], thickness: Number, col: np.ndarray, /, round: bool = True):
        """
        Draw a closed polygon!

        Args:
            ps: The points making up the polygon
            thickness: The thickness of the line. Must be > 0.
            col: The colour of the line

        Keyword args:
            round: Whether the line ends are round or not
        """
        if thickness <= 0:
            raise ValueError(
                'Line has to have a thickness of greater than 0!'
            )
        self.ps = np.array(ps)
        assert len(self.ps.shape) == 2, "Points must be a 2 dimensional array; [(point 1 x, point 1 y), (point 2 x, point 2 y), etc.]"
        assert self.ps.shape[1] == 2, "Points must have only 2 dimensions; an x and a y; [(point 1 x, point 1 y), etc.]"
        assert thickness > 0, "Thickness must be >0"
        self.thickness = thickness
        self.col = np.array(col, np.uint8)
        assert self.col.shape == (4,), "Colour is of incorrect shape!"
        self.flags = OpFlags.Transformable
        self.round = round
    
    def applyTrans(self, mat: np.ndarray, arr: np.ndarray) -> np.ndarray:
        ps = self.ps
        if len(ps) < 2:
            return
        s = np.linalg.svd(mat[:2, :2], compute_uv=False)
        t = self.thickness * np.mean(s)
        newps = self._warpPs(mat, ps)
        if self.round:
            ht = t//2
            for p in newps:
                _drawCirc(arr, p, ht, 0, self.col)
        if len(ps) == 2:
            _drawThickLine(arr, newps[0], newps[1], t, self.col)
            return arr
        p1 = newps[0]
        for p2 in newps[1:]:
            _drawThickLine(arr, p1, p2, t, self.col)
            p1 = p2
        _drawThickLine(arr, p1, newps[0], t, self.col)
        return arr

class Line(Polygon):
    @overload
    def __init__(self, p1: Point, p2: Point, thickness: Number, col: np.ndarray, /, round: bool = True):
        """
        Draw a line!

        Args:
            p1: The starting point of the line (must be in format `[x, y]`)
            p2: The ending point of the line (must be in format `[x, y]`)
            thickness: The thickness of the line. Must be > 0.
            col: The colour of the line

        Keyword args:
            round: Whether the line ends are round or not
        """
    @overload
    def __init__(self, ps: Iterable[Point], thickness: Number, col: np.ndarray, /, round: bool = True):
        """
        Draw a line!

        Args:
            ps: The points of the line (must be in format `[[x1, y1], [x2, y2]]`)
            thickness: The thickness of the line. Must be > 0.
            col: The colour of the line

        Keyword args:
            round: Whether the line ends are round or not
        """
    def __init__(self, *args, round=True):
        if len(args) == 4:
            p1, p2, thickness, col = args
            ps = (p1, p2)
        elif len(args) == 3:
            ps, thickness, col = args
        else:
            raise TypeError(
                f'Incorrect number of arguments! Expected 3 or 4, found {len(args)}!'
            )
        super().__init__(ps, thickness, col, round=round)
        assert self.ps.shape == (2, 2), "Points must be in this format: [(point 1 x, point 1 y), (point 2 x, point 2 y)]"


class Rect(Polygon):
    __slots__ = ['pos', 'sze', 'thickness', 'col']

    @overload
    def __init__(self, pos: Point, sze: Point, thickness: Number, col: np.ndarray, /, roundness: Number = 0, round: bool = True):
        """
        Draws a rectangle!

        Args:
            pos: The position of the rect
            sze: The size of the rect
            thickness: The thickness of the rect. If == 0, will fill the entire rect. Must be >= 0.
            col: The colour of the rect

        Keyword args:
            roundness: The roundness of the rect. 0 = ends of lines rounded, >0 = ends rounded by that many pixels, <0 = do not round the lines at all
            round: Whether to include circles at every joint of the line or not
        """
    @overload
    def __init__(self, x: Number, y: Number, width: Number, height: Number, thickness: Number, col: np.ndarray, /, roundness: Number = 0, round: bool = True):
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
            roundness: The roundness of the rect. 0 = ends of lines rounded, >0 = ends rounded by that many pixels, <0 = do not round the lines at all (doesn't apply when using projection/rotation)
            round: Whether to include circles at every joint of the line or not (only applies when using projection/rotation)
        """
    def __init__(self, *args, roundness = 0, round=True):
        if len(args) == 4:
            self.pos, self.sze, self.thickness, col = args
        elif len(args) == 6:
            x, y, w, h, self.thickness, col = args
            self.pos = (x, y)
            self.sze = (w, h)
        else:
            raise TypeError(
                f'Incorrect number of arguments! Expected 3 or 6, found {len(args)}!'
            )
        assert self.thickness >= 0, "Thickness must be >=0"
        self.round = roundness
        self.col = np.array(col, np.uint8)
        assert self.col.shape == (4,), "Colour is of incorrect shape!"
        self.flags = OpFlags.Transformable
        self.round = round

    @property
    def ps(self):
        return [
            self.pos,
            [self.pos[0], self.pos[1]+self.sze[1]],
            [self.pos[0]+self.sze[0], self.pos[1]+self.sze[1]],
            [self.pos[0]+self.sze[0], self.pos[1]]
        ]

    def applyTrans(self, mat: np.ndarray, arr: np.ndarray) -> np.ndarray:
        # Checks if the rectangle after matrix op is still a rectangle - i.e. no perspective warp or rotation
        if (mat[2] == [0, 0, 1]).all() and \
                ((mat[[0,1], [1,0]] == [0, 0]).all() or (mat[[0,1], [0,1]] == [0, 0]).all()):
            s = np.linalg.svd(mat[:2, :2], compute_uv=False)
            t = self.thickness * np.mean(s)
            newps = self._warpPs(mat, [self.pos, self.sze])
            _drawRect(arr, newps[0], newps[1], t, self.round, self.col)
        else:
            # If not, draw the lines
            super().applyTrans(mat, arr)
        return arr


# TODO: Add an input for rotation
class Elipse(TransOp):
    __slots__ = ['pos', 'xradius', 'yradius', 'thickness', 'col']

    @overload
    def __init__(self, pos: Point, xradius: Number, yradius: Number, thickness: Number, col: np.ndarray):
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
    def __init__(self, x: Number, y: Number, xradius: Number, yradius: Number, thickness: Number, col: np.ndarray):
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
    def __init__(self, *args):
        if len(args) == 6:
            x, y, self.xradius, self.yradius, self.thickness, col = args
            self.pos = (x, y)
        elif len(args) == 5:
            self.pos, self.xradius, self.yradius, self.thickness, col = args
        else:
            raise ValueError(
                f'Expected 5-6 arguments, found {len(args)}!'
            )
        assert self.thickness >= 0, "Thickness must be >=0"
        self.col = np.array(col, np.uint8)
        assert self.col.shape == (4,), "Colour is of incorrect shape!"
        self.flags = OpFlags.Transformable
    
    def applyTrans(self, mat: np.ndarray, arr: np.ndarray) -> np.ndarray:
        if (mat[2] == [0, 0, 1]).all():
            centre = (mat @ [self.pos[0], self.pos[1], 1.0])[:2]
            A = mat[:2, :2]
            u = A @ np.array([1.0, 0.0]) * self.xradius
            v = A @ np.array([0.0, 1.0]) * self.yradius

            r1 = np.hypot(u[0], u[1])
            r2 = np.hypot(v[0], v[1])

            # NOTE: I could have implemented different thickness for both sides of the elipse, but I didn't want to.
            s = np.linalg.svd(A, compute_uv=False)
            t = self.thickness * np.mean(s)
            if r1 == r2:
                _drawCirc(arr, centre, r1, t, self.col)
            else:
                angle = math.atan2(u[1], u[0])
                _drawElipse(arr, centre, r1, r2, angle, t, self.col)
        else:
            if mat[2,2] != 1:
                raise NotImplementedError(
                    'Cannot have a non-normalized homogeneous coordinate with circles yet!'
                )
            raise NotImplementedError(
                'Cannot have projective transform with circles yet!'
            )
        return arr

class Circle(Elipse):
    @overload
    def __init__(self, pos: Point, radius: Number, thickness: Number, col: np.ndarray):
        """
        Draws a circle!

        Args:
            pos: The position of the circle
            radius: The radius of the circle
            thickness: The thickness of the circle. If == 0, will fill the circle entirely. Must be >= 0.
            col: The colour to fill the circle with.
        """
    @overload
    def __init__(self, x: Number, y: Number, radius: Number, thickness: Number, col: np.ndarray):
        """
        Draws a circle! (recommended to use the other definition with `((x, y), ...)` instead of `(x, y, ...)` for readability)

        Args:
            x: The X position of the circle
            y: The y position of the circle
            radius: The radius of the circle
            thickness: The thickness of the circle. If == 0, will fill the circle entirely. Must be >= 0.
            col: The colour to fill the circle with.
        """
    def __init__(self, *args):
        if len(args) == 5:
            x, y, radius, self.thickness, col = args
            self.pos = (x, y)
        elif len(args) == 4:
            self.pos, radius, self.thickness, col = args
        else:
            raise ValueError(
                f'Expected 4-5 arguments, found {len(args)}!'
            )
        assert self.thickness >= 0, "Thickness must be >=0"
        self.xradius, self.yradius = radius, radius
        self.col = np.array(col, np.uint8)
        assert self.col.shape == (4,), "Colour is of incorrect shape!"
        self.flags = OpFlags.Transformable

