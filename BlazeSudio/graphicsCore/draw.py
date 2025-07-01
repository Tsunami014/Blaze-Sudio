import numpy as np
from typing import overload, Iterable
from BlazeSudio.graphicsCore.basebase import Op, ElmOp, Func, OpsList
from numba import njit

@njit
def _drawThickLine(arr, p1, p2, colour, thickness):
    x, y = p1
    x1, y1 = p2
    radius = thickness / 2
    r2 = radius*radius
    dx = abs(x1 - x)
    dy = abs(y1 - y)
    if dx > dy:
        if x > x1:
            x, x1 = x1, x
            y, y1 = y1, y
        sy = 1 if y < y1 else -1
        err = dx / 2
        while x < x1:
            # Draw a filled circle at (x, y)
            for yy in range(round(y - radius), round(y + radius) + 1):
                for xx in range(round(x - radius), round(x + radius) + 1):
                    if (xx - x) ** 2 + (yy - y) ** 2 <= r2:
                        if 0 <= yy < arr.shape[0] and 0 <= xx < arr.shape[1]:
                            arr[yy, xx] = colour
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += 1
    else:
        if y > y1:
            x, x1 = x1, x
            y, y1 = y1, y
        sx = 1 if x < x1 else -1
        err = dy / 2
        while y < y1:
            # Draw a filled circle at (x, y)
            for yy in range(round(y - radius), round(y + radius) + 1):
                for xx in range(round(x - radius), round(x + radius) + 1):
                    if 0 <= yy < arr.shape[0] and 0 <= xx < arr.shape[1]:
                        if (xx - x) ** 2 + (yy - y) ** 2 <= r2:
                            arr[yy, xx] = colour
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += 1

    # Draw one last filled circles at the end
    for yy in range(round(y1 - radius), round(y1 + radius + 1)):
        for xx in range(round(x1 - radius), round(x1 + radius + 1)):
            if (xx - x1) ** 2 + (yy - y1) ** 2 <= r2:
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
    __slots__ = ['pos', 'sze', 'thickness', 'col', 'round']
    def __init__(self, x, y, width, height, thickness, col, roundness):
        self.pos = (x, y)
        self.sze = (width, height)
        assert thickness >= 0, "Thickness must be >=0"
        self.thickness = thickness
        self.col = col
        self.round = roundness

    def ApplyOp(self, op: Op):
        # TODO: transforms
        return True

    def ApplyOnArr(self, arr: np.ndarray):
        h, w = arr.shape

        clip = lambda pos, bound: int(max(min(pos, bound), 0)+0.5)

        if self.sze[0] > 0:
            x0, x1 = self.pos[0],  self.pos[0] + self.sze[0]
        else:
            x0, x1 = self.pos[0] + self.sze[0],  self.pos[0]
        if self.sze[1] > 0:
            y0, y1 = self.pos[1],  self.pos[1] + self.sze[1]
        else:
            y0, y1 = self.pos[1] + self.sze[1],  self.pos[1]

        # Compute actual rounding radius (cannot exceed half-size, nor thickness)
        r = min(self.round,
                (x1 - x0) / 2,
                (y1 - y0) / 2)
        r = max(0, r)

        t = self.thickness

        if t == 0:
            # Fill entire area
            if r == 0:
                # bcos it's faster than otherwise
                arr[clip(y0, h) : clip(y1, h),
                    clip(x0, w) : clip(x1, w)] = self.col
            else:
                arr[clip(y0+r, h) : clip(y1-r, h),
                    clip(x0, w)   : clip(x1, w)] = self.col
                arr[clip(y0, h)   : clip(y1, h),
                    clip(x0+r, w) : clip(x1-r, w)] = self.col
        else:
            # Clip edges for straight sections (excluding corners)
            # Top edge
            arr[clip(y0, h)   : clip(y0+t, h),
                clip(x0+r, w) : clip(x1-r, w)
            ] = self.col
            # Bottom edge
            arr[clip(y1-t, h) : clip(y1, h),
                clip(x0+r, w) : clip(x1-r, w)
            ] = self.col
            # Left edge
            arr[clip(y0+r, h) : clip(y1-r, h),
                clip(x0,w)    : clip(x0+t, w)
            ] = self.col
            # Right edge
            arr[clip(y0+r, h) : clip(y1-r, h),
                clip(x1-t, w) : clip(x1, w)
            ] = self.col

        if r > 0:
            r2 = r*r
            off = 0
            if t == 0:
                rthic2 = 0
                off = 1
            else:
                rthic2 = (r - t) * (r - t)

            # draw quarter-circles at the four corners
            for cx, cy, xs, xe, ys, ye in [
                (x0 + r - off, y0 + r - 1,       x0,     x0 + r, y0,     y0 + r),  # TL
                (x1 - r,       y0 + r - 1,       x1 - r, x1,     y0,     y0 + r),  # TR
                (x0 + r - off, y1 - r - 1 + off, x0,     x0 + r, y1 - r, y1),      # BL
                (x1 - r,       y1 - r - 1 + off, x1 - r, x1,     y1 - r, y1)       # BR
            ]:
                xs, xe = clip(xs, w), clip(xe, w)
                ys, ye = clip(ys, h), clip(ye, h)
                for yy in range(ys, ye):
                    dy2 = (yy - cy) ** 2
                    for xx in range(xs, xe):
                        d2 = (xx - cx) ** 2 + dy2
                        # only paint the annulus between r-t and r
                        if rthic2 <= d2 < r2:
                            arr[yy, xx] = self.col

class _CircleOp(ElmOp):
    __slots__ = ['pos', 'radius', 'thickness', 'col']
    def __init__(self, pos, radius, thickness, col):
        self.pos = pos
        self.radius = abs(radius)
        assert thickness >= 0, "Thickness must be >=0"
        self.thickness = thickness
        self.col = col
 
    def ApplyOp(self, op: Op):
        # TODO: transforms
        return True

    def ApplyOnArr(self, arr: np.ndarray):
        h, w = arr.shape

        x, y = self.pos

        limit = lambda x, bound: int(max(min(x, bound), 0)+0.5)
        x_min = limit(x - self.radius - 1, w)
        x_max = limit(x + self.radius + 1, w)
        y_min = limit(y - self.radius - 1, h)
        y_max = limit(y + self.radius + 1, h)

        radius_outer_sq = self.radius ** 2
        if self.thickness == 0:
            radius_inner_sq = 0
        else:
            radius_inner_sq = max(self.radius - self.thickness, 0) ** 2

        for yy in range(y_min, y_max):
            dy = yy - y
            for xx in range(x_min, x_max):
                dx = xx - x
                dist_sq = dx * dx + dy * dy

                if radius_inner_sq <= dist_sq <= radius_outer_sq:
                    arr[yy, xx] = self.col


class _ElipseOp(ElmOp):
    __slots__ = ['pos', 'xradius', 'yradius', 'thickness', 'col']
    def __init__(self, pos, xradius, yradius, thickness, col):
        self.pos = pos
        self.xradius = abs(xradius)
        self.yradius = abs(yradius)
        assert thickness >= 0, "Thickness must be >=0"
        self.thickness = thickness
        self.col = col
 
    def ApplyOp(self, op: Op):
        # TODO: transforms
        return True

    def ApplyOnArr(self, arr: np.ndarray):
        h, w = arr.shape

        x, y = self.pos

        if self.thickness >= min(self.xradius, self.yradius):
            t = 0
        else:
            t = self.thickness/2

        limit = lambda x, bound: int(max(min(x, bound), 0)+0.5)
        x_min = limit(x - self.xradius - 1 - t, w)
        x_max = limit(x + self.xradius + 1 + t, w)
        y_min = limit(y - self.yradius - 1 - t, h)
        y_max = limit(y + self.yradius + 1 + t, h)

        if self.thickness == 0 or self.thickness >= min(self.xradius, self.yradius):
            xd = self.xradius * self.xradius
            yd = self.yradius * self.yradius

            for yy in range(y_min, y_max):
                dy = yy - y
                dy = dy * dy
                for xx in range(x_min, x_max):
                    dx = xx - x
                    dx = dx * dx

                    if dx/xd + dy/yd <= 1:
                        arr[yy, xx] = self.col
        else:
            xd1 = self.xradius - t
            xd1 = xd1 * xd1
            yd1 = self.yradius - t
            yd1 = yd1 * yd1
            xd2 = self.xradius + t
            xd2 = xd2 * xd2
            yd2 = self.yradius + t
            yd2 = yd2 * yd2

            for yy in range(y_min, y_max):
                dy = yy - y
                dy = dy * dy
                for xx in range(x_min, x_max):
                    dx = xx - x
                    dx = dx * dx

                    if dx/xd2 + dy/yd2 <= 1 <= dx/xd1 + dy/yd1:
                        arr[yy, xx] = self.col

class _DrawFuncs(Func):
    # TODO: Overload for lines
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
    def drawRect(self, pos: Iterable[int|float], sze: Iterable[int|float], thickness: int|float, col: int, /, roundness: int|float = 0):
        """
        Draws a rectangle

        Args:
            pos: The position of the rect
            sze: The size of the rect
            thickness: The thickness of the rect. If == 0, will fill the entire rect. Must be >= 0.
            col: The colour of the rect

        Keyword args:
            roundness: The roundness of the rect. 0 = ends of lines rounded, >0 = ends rounded by that many pixels, <0 = do not round the lines at all
        """
    @overload
    def drawRect(self, x: int|float, y: int|float, width: int|float, height: int|float, thickness: int|float, col: int, /, roundness: int|float = 0):
        """
        Draws a rectangle

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
    def drawRect(self, *args, roundness = 0):
        if len(args) == 4:
            self._ops.append(_RectOp(args[0][0], args[0][1], args[1][0], args[1][1], args[2], args[3], roundness))
        elif len(args) == 6:
            self._ops.append(_RectOp(*args, roundness=roundness))
        else:
            raise ValueError(
                f'Expected 4/6 args, found {len(args)}!'
            )

    @overload
    def drawCircle(self, pos: Iterable[int|float], radius: int|float, thickness: int|float, col: int):
        """
        Draws a circle!

        Args:
            pos: The position of the circle
            radius: The radius of the circle
            thickness: The thickness of the circle. If == 0, will fill the circle entirely. Must be >= 0.
            col: The colour to fill the circle with.
        """
    @overload
    def drawCircle(self, x: int|float, y: int|float, radius: int|float, thickness: int|float, col: int):
        """
        Draws a circle!

        Args:
            x: The X position of the circle
            y: The y position of the circle
            radius: The radius of the circle
            thickness: The thickness of the circle. If == 0, will fill the circle entirely. Must be >= 0.
            col: The colour to fill the circle with.
        """
    def drawCircle(self, *args):
        if len(args) == 5:
            self._ops.append(_CircleOp((args[0], args[1]), args[2], args[3], args[4]))
        elif len(args) == 4:
            self._ops.append(_CircleOp(*args))
        else:
            raise ValueError(
                f'Expected 4-5 arguments, found {len(args)}!'
            )

    @overload
    def drawElipse(self, pos: Iterable[int|float], xradius: int|float, yradius: int|float, thickness: int|float, col: int):
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
    def drawElipse(self, x: int|float, y: int|float, xradius: int|float, yradius: int|float, thickness: int|float, col: int):
        """
        Draws an elipse!

        Args:
            x: The X position of the elipse
            y: The y position of the elipse
            xradius: The radius of the width of the elipse
            yradius: The radius of the height of the elipse
            thickness: The thickness of the circle. If == 0, will fill the circle entirely. Must be >= 0.
            col: The colour to fill the circle with.
        """
    def drawElipse(self, *args):
        if len(args) == 6:
            self._ops.append(_ElipseOp((args[0], args[1]), args[2], args[3], args[4], args[5]))
        elif len(args) == 5:
            self._ops.append(_ElipseOp(*args))
        else:
            raise ValueError(
                f'Expected 5-6 arguments, found {len(args)}!'
            )

