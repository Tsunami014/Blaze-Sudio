import numpy as np
from typing import overload, Iterable, Tuple
from BlazeSudio.graphicsCore.basebase import Op, ElmOp, Func, OpsList
from BlazeSudio.speedup import jitrix


@jitrix('draw', '(np.full((100, 100), 0, np.uint32), (10, 10), (80, 80), 10, 5.0)')
def _drawThickLine(arr: 'np.uint32[:, :]', p1: Tuple[int, int], p2: Tuple[int, int], colour: np.uint32, thickness: int):
    x, y = p1
    x1, y1 = p2
    radius = int(thickness / 2)
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
            for yy in range(y - radius, y + radius + 1):
                for xx in range(x - radius, x + radius + 1):
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
            for yy in range(y - radius, y + radius + 1):
                for xx in range(x - radius, x + radius + 1):
                    if 0 <= yy < arr.shape[0] and 0 <= xx < arr.shape[1]:
                        if (xx - x) ** 2 + (yy - y) ** 2 <= r2:
                            arr[yy, xx] = colour
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += 1

    # Draw one last filled circles at the end
    for yy in range(y1 - radius, y1 + radius + 1):
        for xx in range(x1 - radius, x1 + radius + 1):
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

@jitrix('draw', '(np.full((100, 100), 0, np.uint32), (10, 10), (80, 80), 10, 5, 500)')
def _applyRect(arr: 'np.uint32[:, :]', pos: Tuple[int, int], sze: Tuple[int, int], thickness: int, round: int, col: np.uint32):
    h, w = arr.shape

    if sze[0] > 0:
        x0, x1 = pos[0], pos[0] + sze[0]
    else:
        x0, x1 = pos[0] + sze[0], pos[0]
    if sze[1] > 0:
        y0, y1 = pos[1], pos[1] + sze[1]
    else:
        y0, y1 = pos[1] + sze[1], pos[1]

    # Compute actual rounding radius (cannot exceed half-size, nor thickness)
    r = min(round,
            (x1 - x0) / 2,
            (y1 - y0) / 2)
    r = max(0, r)
    t = thickness

    if t <= 0:
        # Fill entire area
        if r == 0:
            # bcos it's faster than otherwise
            a, b = np.clip(np.array([y0, y1]), 0, h)
            c, d = np.clip(np.array([x0, x1]), 0, w)
            arr[a : b, c : d] = col
        else:
            a, b, e, f = np.clip(np.array([y0+r, y1-r, y0, y1]), 0, h)
            c, d, g, h = np.clip(np.array([x0, x1, x0+r, x1-1]), 0, w)
            arr[a : b, c : d] = col
            arr[e : f, g : h] = col
    else:
        # Clip edges for straight sections (excluding corners)
        xs = np.clip(np.array([
            x0, x0+t,
            x1-t, x1,
            x0+r, x1-r,
        ]), 0, w)
        ys = np.clip(np.array([
            y0, y0+t,
            y1-t, y1,
            y0+r, y1-r,
        ]), 0, h)
        # Top edge
        arr[ys[0] : ys[1], xs[4] : xs[5]] = col
        # Bottom edge
        arr[ys[2] : ys[3], xs[4] : xs[5]] = col
        # Left edge
        arr[ys[4] : ys[5], xs[0] : xs[1]] = col
        # Right edge
        arr[ys[4] : ys[5], xs[2] : xs[3]] = col

    if r > 0:
        r2 = r*r
        off = 0
        if t == 0:
            rthic2 = 0
            off = 1
        else:
            rthic2 = (r - t) * (r - t)

        xs = np.clip(np.array([
            x0, x0 + r,
            x1 - r, x1
        ]), 0, w)
        ys = np.clip(np.array([
            y0, y0 + r,
            y1 - r, y1
        ]), 0, h)
        # draw quarter-circles at the four corners
        for cx, cy, xs, xe, ys, ye in [
            (x0 + r - off, y0 + r - 1,       xs[0], xs[1], ys[0], ys[1]),  # TL
            (x1 - r,       y0 + r - 1,       xs[2], xs[3], ys[0], ys[1]),  # TR
            (x0 + r - off, y1 - r - 1 + off, xs[0], xs[1], ys[2], ys[3]),  # BL
            (x1 - r,       y1 - r - 1 + off, xs[2], xs[3], ys[2], ys[3])   # BR
        ]:
            for yy in range(ys, ye):
                dy2 = (yy - cy) ** 2
                for xx in range(xs, xe):
                    d2 = (xx - cx) ** 2 + dy2
                    # only paint the annulus between r-t and r
                    if rthic2 <= d2 < r2:
                        arr[yy, xx] = col

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
        _applyRect(arr, self.pos, self.sze, self.thickness, self.round, self.col)

@jitrix('draw', '(np.full((100, 100), 0, np.uint32), (50, 60), 40, 10, 345)')
def _applyCirc(arr: 'np.uint32[:, :]', pos: Tuple[int, int], radius: int, thickness: int, col: np.uint32):
    h, w = arr.shape

    x, y = pos

    x_min = max(min(x - radius - 1, w), 0)
    x_max = max(min(x + radius + 1, w), 0)
    y_min = max(min(y - radius - 1, h), 0)
    y_max = max(min(y + radius + 1, h), 0)

    radius_outer_sq = radius ** 2
    if thickness == 0:
        radius_inner_sq = 0
    else:
        radius_inner_sq = max(radius - thickness, 0) ** 2

    for yy in range(y_min, y_max):
        dy = yy - y
        for xx in range(x_min, x_max):
            dx = xx - x
            dist_sq = dx * dx + dy * dy

            if radius_inner_sq <= dist_sq <= radius_outer_sq:
                arr[yy, xx] = col

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
        _applyCirc(arr, self.pos, self.radius, self.thickness, self.col)


@jitrix('draw', '(np.full((100, 100), 0, np.uint32), (50, 50), 40, 30, 10, 5)')
def _applyElipse(arr: 'np.uint32[:, :]', pos: Tuple[int, int], xradius: int, yradius: int, thickness: int, col: np.uint32):
    h, w = arr.shape

    x, y = pos

    if thickness >= min(xradius, yradius):
        t = 0
    else:
        t = thickness//2

    x_min = max(min(x - xradius - 1 - t, w), 0)
    x_max = max(min(x + xradius + 1 + t, w), 0)
    y_min = max(min(y - yradius - 1 - t, h), 0)
    y_max = max(min(y + yradius + 1 + t, h), 0)

    if thickness == 0 or thickness >= min(xradius, yradius):
        xd = xradius * xradius
        yd = yradius * yradius

        for yy in range(y_min, y_max):
            dy = yy - y
            dy = dy * dy
            for xx in range(x_min, x_max):
                dx = xx - x
                dx = dx * dx

                if dx/xd + dy/yd <= 1:
                    arr[yy, xx] = col
    else:
        xd1 = xradius - t
        xd1 = xd1 * xd1
        yd1 = yradius - t
        yd1 = yd1 * yd1
        xd2 = xradius + t
        xd2 = xd2 * xd2
        yd2 = yradius + t
        yd2 = yd2 * yd2

        for yy in range(y_min, y_max):
            dy = yy - y
            dy = dy * dy
            for xx in range(x_min, x_max):
                dx = xx - x
                dx = dx * dx

                if dx/xd2 + dy/yd2 <= 1 <= dx/xd1 + dy/yd1:
                    arr[yy, xx] = col

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
        _applyElipse(arr, self.pos, self.xradius, self.yradius, self.thickness, self.col)

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

