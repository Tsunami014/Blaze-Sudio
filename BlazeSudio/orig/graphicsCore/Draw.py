from typing import overload, Iterable, Tuple
from .base import OpFlags, TransOp
import numpy as np
import math

Number = int|float
Point = Tuple[Number, Number]

def _drawThickLine(arr: np.ndarray, p1: np.ndarray, p2: np.ndarray, thickness: int, colour: np.ndarray):
    x, y = p1.astype(np.int64)
    x1, y1 = p2.astype(np.int64)
    radius = int(thickness) // 2

    # Precompute circle mask
    yy, xx = np.ogrid[-radius:radius+1, -radius:radius+1]
    circle_mask = xx**2 + yy**2 <= radius**2

    dx = abs(x1 - x)
    dy = abs(y1 - y)
    if dx > dy:
        if x > x1:
            x, x1 = x1, x
            y, y1 = y1, y
        sy = 1 if y < y1 else -1
        err = dx / 2
        while x <= x1:
            y_indices = np.arange(y-radius, y+radius+1)
            x_indices = np.arange(x-radius, x+radius+1)
            valid_y = (y_indices >= 0) & (y_indices < arr.shape[0])
            valid_x = (x_indices >= 0) & (x_indices < arr.shape[1])
            arr[np.ix_(y_indices[valid_y], x_indices[valid_x])][circle_mask[valid_y][:, valid_x]] = colour
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
        while y <= y1:
            y_indices = np.arange(y-radius, y+radius+1)
            x_indices = np.arange(x-radius, x+radius+1)
            valid_y = (y_indices >= 0) & (y_indices < arr.shape[0])
            valid_x = (x_indices >= 0) & (x_indices < arr.shape[1])
            arr[np.ix_(y_indices[valid_y], x_indices[valid_x])][circle_mask[valid_y][:, valid_x]] = colour
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += 1

class Polygon(TransOp):
    __slots__ = ['ps', 'thickness', 'col']
    def __init__(self, ps: Iterable[Point], thickness: Number, col: np.ndarray):
        """
        Draw a closed polygon!

        Args:
            ps: The points making up the polygon
            thickness: The thickness of the line. Must be > 0.
            col: The colour of the line
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
    
    def applyTrans(self, mat: np.ndarray, arr: np.ndarray) -> np.ndarray:
        if len(self.ps) < 2:
            return
        s = np.linalg.svd(mat[:2, :2], compute_uv=False)
        t = self.thickness * np.mean(s)
        newps = self._warpPs(mat, self.ps)
        p1 = newps[0]
        for p2 in newps[1:]:
            _drawThickLine(arr, p1, p2, t, self.col)
            p1 = p2
        p2 = newps[0]
        _drawThickLine(arr, p1, p2, t, self.col)
        return arr

class Line(Polygon):
    @overload
    def __init__(self, p1: Point, p2: Point, thickness: Number, col: np.ndarray):
        """
        Draw a line!

        Args:
            p1: The starting point of the line (must be in format `[x, y]`)
            p2: The ending point of the line (must be in format `[x, y]`)
            thickness: The thickness of the line. Must be > 0.
            col: The colour of the line
        """
    @overload
    def __init__(self, ps: Iterable[Point], thickness: Number, col: np.ndarray):
        """
        Draw a line!

        Args:
            ps: The points of the line (must be in format `[[x1, y1], [x2, y2]]`)
            thickness: The thickness of the line. Must be > 0.
            col: The colour of the line
        """
    def __init__(self, *args):
        if len(args) == 4:
            p1, p2, thickness, col = args
            ps = (p1, p2)
        elif len(args) == 3:
            ps, thickness, col = args
        else:
            raise TypeError(
                f'Incorrect number of arguments! Expected 3 or 4, found {len(args)}!'
            )
        super().__init__(ps, thickness, col)
        assert self.ps.shape == (2, 2), "Points must be in this format: [(point 1 x, point 1 y), (point 2 x, point 2 y)]"

    def applyTrans(self, mat: np.ndarray, arr: np.ndarray) -> np.ndarray:
        newps = self._warpPs(mat, self.ps)
        s = np.linalg.svd(mat[:2, :2], compute_uv=False)
        _drawThickLine(arr, newps[0], newps[1], self.thickness * np.mean(s), self.col)
        return arr


def _drawRect(arr: np.ndarray, pos: np.ndarray, sze: np.ndarray, thickness: int, round: int, col: np.ndarray):
    h, w, _ = arr.shape
    pos, sze = pos.astype(np.int64), sze.astype(np.int64)
    if sze[0] > 0:
        x0, x1 = pos[0], pos[0] + sze[0]
    else:
        x0, x1 = pos[0] + sze[0], pos[0]
    if sze[1] > 0:
        y0, y1 = pos[1], pos[1] + sze[1]
    else:
        y0, y1 = pos[1] + sze[1], pos[1]

    # Compute actual rounding radius (cannot exceed half-size, nor thickness)
    r = min(int(round),
            (x1 - x0) // 2,
            (y1 - y0) // 2)
    r = max(0, r)
    t = int(thickness)

    if t <= 0:
        # Fill entire area
        if r <= 0:
            # bcos it's faster than otherwise
            a, b = np.clip(np.array([y0, y1]), 0, h)
            c, d = np.clip(np.array([x0, x1]), 0, w)
            arr[a : b, c : d, :] = col
            return
        else:
            a, b, e, f = np.clip(np.array([y0+r, y1-r, y0, y1]), 0, h)
            c, d, g, h = np.clip(np.array([x0, x1, x0+r, x1-1]), 0, w)
            arr[a : b, c : d, :] = col
            arr[e : f, g : h, :] = col
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
        
        arr[ys[0] : ys[1], xs[4] : xs[5], :] = col  # Top edge
        arr[ys[2] : ys[3], xs[4] : xs[5], :] = col  # Bottom edge
        arr[ys[4] : ys[5], xs[0] : xs[1], :] = col  # Left edge
        arr[ys[4] : ys[5], xs[2] : xs[3], :] = col  # Right edge

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
            yy, xx = np.ogrid[ys:ye, xs:xe]
            d2 = (xx - cx)**2 + (yy - cy)**2
            mask = (rthic2 <= d2) & (d2 < r2)
            arr[ys:ye, xs:xe][mask] = col

class Rect(TransOp):
    __slots__ = ['pos', 'sze', 'thickness', 'col', 'round']

    @overload
    def __init__(self, pos: Point, sze: Point, thickness: Number, col: np.ndarray, /, roundness: Number = 0):
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
    def __init__(self, x: Number, y: Number, width: Number, height: Number, thickness: Number, col: np.ndarray, /, roundness: Number = 0):
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
    def __init__(self, *args, roundness = 0):
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

    def applyTrans(self, mat: np.ndarray, arr: np.ndarray) -> np.ndarray:
        s = np.linalg.svd(mat[:2, :2], compute_uv=False)
        t = self.thickness * np.mean(s)

        # Checks if the rectangle after matrix op is still a rectangle - i.e. no perspective warp or rotation
        if (mat[2] == [0, 0, 1]).all() and \
                ((mat[[0,1], [1,0]] == [0, 0]).all() or (mat[[0,1], [0,1]] == [0, 0]).all()):
            newps = self._warpPs(mat, [self.pos, self.sze])
            _drawRect(arr, newps[0], newps[1], t, self.round, self.col)
        else:
            # If not, draw the lines
            newps = self._warpPs(mat, [
                self.pos,
                [self.pos[0], self.pos[1]+self.sze[1]],
                [self.pos[0]+self.sze[0], self.pos[1]+self.sze[1]],
                [self.pos[0]+self.sze[0], self.pos[1]]
            ])
            p1 = newps[0]
            for p2 in newps[1:]:
                _drawThickLine(arr, p1, p2, t, self.col)
                p1 = p2
            p2 = newps[0]
            _drawThickLine(arr, p1, p2, t, self.col)
        return arr


def _drawCirc(arr: np.ndarray, pos: np.ndarray, radius: int, thickness: int, col: np.ndarray):
    r = int(radius)
    h, w, _ = arr.shape
    x, y = pos.astype(np.int64)

    # Bounding box
    rng = (
        slice(max(y - r - 1, 0),min(y + r + 1, h)),
        slice(max(x - r - 1, 0),min(x + r + 1, w))
    )

    # Radii squared
    radius_outer_sq = r ** 2
    radius_inner_sq = 0 if thickness == 0 else max(r - thickness, 0) ** 2

    # Coordinate grid
    yy, xx = np.mgrid[rng]
    dx = xx - x
    dy = yy - y
    dist_sq = dx**2 + dy**2

    mask = (radius_inner_sq <= dist_sq) & (dist_sq <= radius_outer_sq)
    arr[rng][mask] = col

def _drawElipse(arr: np.ndarray, pos: np.ndarray, xradius: int, yradius: int, rotation: float, thickness: int, col: np.ndarray):
    xrad, yrad = int(xradius), int(yradius)
    h, w, _ = arr.shape
    x, y = pos.astype(np.int64)

    if thickness >= min(xrad, yrad):
        t = 0
    else:
        t = int(thickness) // 2

    # Bounding box
    x_min = max(x - xrad- 1 - t, 0)
    x_max = min(x + xrad+ 1 + t, w)
    y_min = max(y - yrad- 1 - t, 0)
    y_max = min(y + yrad+ 1 + t, h)

    # Coordinate grid
    yy, xx = np.mgrid[y_min:y_max, x_min:x_max]
    dx = xx - x
    dy = yy - y

    # Rotation
    cos_t = np.cos(rotation)
    sin_t = np.sin(rotation)
    xr = dx * cos_t + dy * sin_t
    yr = -dx * sin_t + dy * cos_t

    # Ellipse equation
    if thickness == 0 or thickness >= min(xrad, yrad):
        mask = (xr**2 / xrad**2 + yr**2 / yrad**2) <= 1
    else:
        outer = (xr**2 / (xrad+ t)**2 + yr**2 / (yrad+ t)**2) <= 1
        inner = (xr**2 / (xrad- t)**2 + yr**2 / (yrad- t)**2) <= 1
        mask = outer & ~inner

    # Apply color
    arr[y_min:y_max, x_min:x_max][mask] = col

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

