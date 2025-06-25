import numpy as np
from typing import overload, Iterable, TYPE_CHECKING
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
        assert thickness > 0, "Thickness must be >0"
        self.thickness = thickness
        self.col = col
    
    def ApplyOp(self, op: Op):
        # TODO: transforms
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
        assert thickness > 0, "Thickness must be >0"
        self.thickness = thickness
        self.col = col
    
    def ApplyOnArr(self, arr: np.ndarray):
        _drawThickLine(arr, self.ps[0], self.ps[1], self.col, self.thickness)

class _RectOp(ElmOp):
    __slots__ = ['pos', 'sze', 'thickness', 'col']
    def __init__(self, x, y, width, height, thickness, col):
        self.pos = (x, y)
        self.sze = (width, height)
        assert thickness > 0, "Thickness must be >0"
        self.thickness = thickness
        self.col = col

    def ApplyOp(self, op: Op):
        # TODO: transforms
        return True

    def ApplyOnArr(self, arr: np.ndarray):
        h, w = arr.shape

        clip = lambda pos, bound: max(min(pos, bound), 0)

        x0, x1 = sorted((self.pos[0], self.pos[0]+self.sze[0]))
        y0, y1 = sorted((self.pos[1], self.pos[1]+self.sze[1]))

        # Top
        arr[clip(y0, h):clip(y0+self.thickness, h), clip(x0, w):clip(x1+1, w)] = self.col
        # Bottom
        arr[clip(y1-self.thickness+1, h):clip(y1+1, h), clip(x0, w):clip(x1+1, w)] = self.col
        # Left
        arr[clip(y0+self.thickness, h):clip(y1-self.thickness+1, h), clip(x0, w):clip(x0+self.thickness, w)] = self.col
        # Right
        arr[clip(y0+self.thickness, h):clip(y1-self.thickness+1, h), clip(x1-self.thickness+1, w):clip(x1+1, w)] = self.col

def line(sur: 'Surface', p1: Iterable[int|float], p2: Iterable[int|float], thickness: int|float, col: int):
    """
    Draw a line

    Args:
        p1 (Iterable[int | float]): The starting point of the line
        p2 (Iterable[int | float]): The ending point of the line
        thickness (int | float): The thickness of the line. Must be > 0.
        col (int): The colour of the line
    """
    sur.drawLine(p1, p2, thickness, col)
def polygon(sur: 'Surface', ps: Iterable[Iterable[int|float]], thickness: int|float, col: int):
    """
    Draw a closed polygon

    Args:
        ps (Iterable[Iterable[int | float]]): The points making up the polygon
        thickness (int | float): The thickness of the line. Must be > 0.
        col (int): The colour of the line
    """
    sur.drawPolygon(ps, thickness, col)

@overload
def rect(sur: 'Surface', pos: Iterable[int|float], sze: Iterable[int|float], thickness: int|float, col: int):
    """
    Draws a rectangle

    Args:
        pos: The position of the rect
        sze: The size of the rect
        thickness: The thickness of the rect. Must be > 0.
        col: The colour of the rect
    """
@overload
def rect(sur: 'Surface', x: int|float, y: int|float, width: int|float, height: int|float, thickness: int|float, col: int):
    """
    Draws a rectangle

    Args:
        x: The x position of the rect
        y: The y position of the rect
        width: The width of the rect
        height: The height of the rect
        thickness: The thickness of the rect. Must be > 0.
        col: The colour of the rect
    """
def rect(sur: 'Surface', *args):
    sur.drawRect(*args)

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

    @overload
    def drawRect(self, pos: Iterable[int|float], sze: Iterable[int|float], thickness: int|float, col: int):
        """
        Draws a rectangle

        Args:
            pos: The position of the rect
            sze: The size of the rect
            thickness: The thickness of the rect. Must be > 0.
            col: The colour of the rect
        """
    @overload
    def drawRect(self, x: int|float, y: int|float, width: int|float, height: int|float, thickness: int|float, col: int):
        """
        Draws a rectangle

        Args:
            x: The x position of the rect
            y: The y position of the rect
            width: The width of the rect
            height: The height of the rect
            thickness: The thickness of the rect. Must be > 0.
            col: The colour of the rect
        """
    def drawRect(self, *args):
        if len(args) == 4:
            self._ops.append(_RectOp(args[0][0], args[0][1], args[1][0], args[1][1], args[2], args[3]))
        elif len(args) == 6:
            self._ops.append(_RectOp(*args))
        else:
            raise ValueError(
                f'Expected 4/6 args, found {len(args)}!'
            )

