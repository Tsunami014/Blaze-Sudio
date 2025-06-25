import numpy as np
from typing import Iterable, TYPE_CHECKING
from BlazeSudio.graphicsCore.basebase import Op, ElmOp, Func, OpsList
from numba import njit

if TYPE_CHECKING:
    from BlazeSudio.graphicsCore import Surface

# This is so you can use 'graphicsCore.draw.line' in replacement of pygame's 'pygame.draw.line'
__all__ = [
    'line',
    'polygon'
]

@njit
def _drawThickLine(arr, p1, p2, colour, thickness):
    x0, y0 = p1
    x1, y1 = p2
    radius = thickness // 2
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    if dx > dy:
        err = dx // 2
        while x != x1:
            # Draw a filled circle at (x, y)
            for yy in range(y - radius, y + radius + 1):
                for xx in range(x - radius, x + radius + 1):
                    if (xx - x) ** 2 + (yy - y) ** 2 <= radius ** 2:
                        if 0 <= yy < arr.shape[0] and 0 <= xx < arr.shape[1]:
                            arr[yy, xx] = colour
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy // 2
        while y != y1:
            # Draw a filled circle at (x, y)
            for yy in range(int(y - radius), int(y + radius + 1)):
                for xx in range(int(x - radius), int(x + radius + 1)):
                    if (xx - x) ** 2 + (yy - y) ** 2 <= radius ** 2:
                        if 0 <= yy < arr.shape[0] and 0 <= xx < arr.shape[1]:
                            arr[yy, xx] = colour
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    # Draw at the last point
    for yy in range(int(y1 - radius), int(y1 + radius + 1)):
        for xx in range(int(x1 - radius), int(x1 + radius + 1)):
            if (xx - x1) ** 2 + (yy - y1) ** 2 <= radius ** 2:
                if 0 <= yy < arr.shape[0] and 0 <= xx < arr.shape[1]:
                    arr[yy, xx] = colour

class _PolygonOp(ElmOp):
    __slots__ = ['ps', 'thickness', 'col']
    typ = OpsList.Poly
    def __init__(self, ps, thickness, col):
        self.ps = np.array(ps, dtype=np.float64)
        assert len(self.ps.shape) == 2, "Points must be a 2 dimensional array; [(point 1 x, point 1 y), (point 2 x, point 2 y), etc.]"
        assert self.ps.shape[1] == 2, "Points must have only 2 dimensions; an x and a y; [(point 1 x, point 1 y), etc.]"
        self.thickness = thickness
        assert isinstance(col, int)
        self.col = col
    
    def ApplyOp(self, op: Op):
        # TODO: Crop based on screen size
        return True
    def ApplyOnArr(self, arr: np.ndarray):
        if len(self.ps) < 2:
            return
        p1 = self.ps[0]
        for i in range(1, len(self.ps)):
            p2 = self.ps[i]
            _drawThickLine(arr, p1, p2, self.col, self.thickness)
            p1 = p2
        p2 = self.ps[0]
        _drawThickLine(arr, p1, p2, self.col, self.thickness)

class _LineOp(_PolygonOp):
    def __init__(self, p1, p2, thickness, col):
        self.ps = np.array([p1, p2], dtype=np.float64)
        assert self.ps.shape == (2, 2), "Points must have only 2 dimensions; an x and a y; [(point 1 x, point 1 y), (point 2 x, point 2 y)]"
        assert isinstance(col, int)
        self.thickness = thickness
        self.col = col
    
    def ApplyOnArr(self, arr: np.ndarray):
        _drawThickLine(arr, self.ps[0], self.ps[1], self.col, self.thickness)


def line(sur: 'Surface', p1: Iterable[int|float], p2: Iterable[int|float], thickness: int|float, col: int):
    sur.drawLine(p1, p2, thickness, col)
def polygon(sur: 'Surface', ps: Iterable[Iterable[int|float]], thickness: int|float, col: int):
    sur.drawPolygon(ps, thickness, col)


class _DrawFuncs(Func):
    def drawLine(self, p1: Iterable[int|float], p2: Iterable[int|float], thickness: int|float, col: int):
        """
        Draw a line

        Args:
            p1 (Iterable[int | float]): The starting point of the line
            p2 (Iterable[int | float]): The ending point of the line
            thickness (int | float): The thickness of the line. Must be > 0.
            col (int): The colour of the line
        """
        if thickness <= 0:
            raise ValueError(
                'Line has to have a thickness of greater than 0!'
            )
        self._ops.append(_LineOp(p1, p2, thickness, col))
    
    def drawPolygon(self, ps: Iterable[Iterable[int|float]], thickness: int|float, col: int):
        """
        Draw a closed polygon

        Args:
            ps (Iterable[Iterable[int | float]]): The points making up the polygon
            thickness (int | float): The thickness of the line. Must be > 0.
            col (int): The colour of the line
        """
        if thickness <= 0:
            raise ValueError(
                'Line has to have a thickness of greater than 0!'
            )
        self._ops.append(_PolygonOp(ps, thickness, col))
