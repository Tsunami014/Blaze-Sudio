# cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True
import numpy as np
cimport numpy as cnp


def apply(mat: np.ndarray, arr: np.ndarray, smooth: bool):
    background = 0

    h, w = arr.shape[:2]
    is_color = arr.ndim == 3

    T_inv = np.linalg.inv(mat)

    yy, xx = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
    ones = np.ones_like(xx)
    dst = np.stack([xx, yy, ones], axis=-1)

    src = dst @ T_inv.T
    sx = src[..., 0] / src[..., 2]
    sy = src[..., 1] / src[..., 2]

    if smooth:
        x0 = np.floor(sx).astype(int)
        x1 = x0 + 1
        y0 = np.floor(sy).astype(int)
        y1 = y0 + 1

        wx = sx - x0
        wy = sy - y0

        valid = (x0 >= 0) & (x1 < w) & (y0 >= 0) & (y1 < h)

        if not is_color:
            arr = arr[..., None]

        c00 = arr[y0, x0]
        c10 = arr[y0, x1]
        c01 = arr[y1, x0]
        c11 = arr[y1, x1]

        top = c00 * (1 - wx)[..., None] + c10 * wx[..., None]
        bottom = c01 * (1 - wx)[..., None] + c11 * wx[..., None]
        blended = top * (1 - wy)[..., None] + bottom * wy[..., None]

        out = np.full((*arr.shape[:2], arr.shape[2]), background, dtype=float)
        out[valid] = blended[valid]
        out = out.astype(arr.dtype)

        if not is_color:
            out = out[..., 0]

        return out
    else:
        sx_i = np.rint(sx).astype(int)
        sy_i = np.rint(sy).astype(int)

        out = np.full_like(arr, background)
        mask = (sx_i >= 0) & (sx_i < w) & (sy_i >= 0) & (sy_i < h)

        out[mask] = arr[sy_i[mask], sx_i[mask]]
        return out


def _drawThickLine(
        cnp.ndarray[cnp.uint8_t, ndim=3] arr,
        cnp.ndarray[cnp.double_t, ndim=1] p1,
        cnp.ndarray[cnp.double_t, ndim=1] p2,
        double thickness,
        cnp.ndarray[cnp.uint8_t, ndim=1] colour):
    cdef long x = <long>p1[0]
    cdef long y = <long>p1[1]
    cdef long x1 = <long>p2[0]
    cdef long y1 = <long>p2[1]
    cdef long half = <long>(thickness) >> 1

    cdef long h = arr.shape[0]
    cdef long w = arr.shape[1]

    cdef long dx = abs(x1 - x)
    cdef long dy = abs(y1 - y)
    cdef long err
    cdef long sx, sy
    cdef long y0, y1b, x0, x1b
    cdef long my0, mx0, my1, mx1

    if dx > dy:
        if x > x1:
            x, x1 = x1, x
            y, y1 = y1, y
        sy = 1 if y < y1 else -1
        err = dx // 2
        while x <= x1:
            y0 = max(y - half, 0)
            y1b = min(y + half + 1, h)
            x0 = max(x, 0)
            x1b = min(x + 1, w)

            if x0 < x1b and y0 < y1b:
                arr[y0:y1b, x0:x1b] = colour

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
        err = dy // 2
        while y <= y1:
            y0 = max(y, 0)
            y1b = min(y + 1, h)
            x0 = max(x - half, 0)
            x1b = min(x + half + 1, w)

            if x0 < x1b and y0 < y1b:
                arr[y0:y1b, x0:x1b] = colour

            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += 1


cdef inline long _clip(long v, long lo, long hi):
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v

def _drawRect(
        cnp.ndarray[cnp.uint8_t, ndim=3] arr,
        cnp.ndarray[cnp.double_t, ndim=1] pos,
        cnp.ndarray[cnp.double_t, ndim=1] sze,
        double thickness,
        double round,
        cnp.ndarray[cnp.uint8_t, ndim=1] col):
    cdef long H = arr.shape[0]
    cdef long W = arr.shape[1]
    cdef long t = <long>thickness

    cdef long x0 = <long>pos[0]
    cdef long y0 = <long>pos[1]
    cdef long x1 = x0 + <long>sze[0]
    cdef long y1 = y0 + <long>sze[1]

    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0

    cdef long r = <long>round
    cdef long w = x1 - x0
    cdef long h = y1 - y0

    cdef long hwid = <long>(w * 0.5)
    cdef long hhei = <long>(h * 0.5)
    if r > hwid:
        r = hwid
    if r > hhei:
        r = hhei
    if r < 0:
        r = 0

    if t <= 0:
        if r == 0:
            arr[_clip(y0, 0, H):_clip(y1, 0, H), _clip(x0, 0, W):_clip(x1, 0, W), :] = col
            return

        # Rounded fill (top/bottom strips + middle)
        arr[_clip(y0 + r, 0, H):_clip(y1 - r, 0, H), _clip(x0, 0, W):_clip(x1, 0, W), :] = col
    else:
        arr[_clip(y0, 0, H):_clip(y0 + t, 0, H), x0+r:x1-r, :] = col # Top
        arr[_clip(y1 - t, 0, H):_clip(y1, 0, H), x0+r:x1-r, :] = col # Bottom
        arr[y0+r:y1-r, _clip(x0, 0, W):_clip(x0 + t, 0, W), :] = col # Left
        arr[y0+r:y1-r, _clip(x1 - t, 0, W):_clip(x1, 0, W), :] = col # Right


    cdef long r2, inner, off
    cdef long cx, cy, xs, xe, ys, ye
    cdef long dx, dy, d2
    cdef long x, y, c
    if r > 0:
        r2 = r*r
        inner = (r - t) * (r - t) if t > 0 else 0
        off = 0 if t > 0 else 1

        # TL, TR, BL, BR
        corners = [
            (x0 + r - off, y0 + r - 1, x0, x0+r, y0, y0+r),
            (x1 - r,       y0 + r - 1, x1-r, x1, y0, y0+r),
            (x0 + r - off, y1 - r - 1 + off, x0, x0+r, y1-r, y1),
            (x1 - r,       y1 - r - 1 + off, x1-r, x1, y1-r, y1)
        ]

        for cx, cy, xs, xe, ys, ye in corners:
            xs = _clip(xs, 0, W)
            xe = _clip(xe, 0, W)
            ys = _clip(ys, 0, H)
            ye = _clip(ye, 0, H)

            for y in range(ys, ye):
                dy = y - cy
                for x in range(xs, xe):
                    dx = x - cx
                    d2 = dx*dx + dy*dy
                    if inner <= d2 < r2:
                        for c in range(arr.shape[2]):
                            arr[y, x, c] = col[c]


def _drawCirc(arr: np.ndarray, pos: np.ndarray, radius: int, thickness: int, col: np.ndarray):
    r = int(radius)
    h, w, _ = arr.shape
    x, y = pos.astype(np.int64)

    y0 = max(y - r - 1, 0)
    y1 = min(y + r + 1, h)
    x0 = max(x - r - 1, 0)
    x1 = min(x + r + 1, w)
    if y0 >= y1 or x0 >= x1:
        return

    # Radii squared
    radius_outer_sq = r ** 2
    radius_inner_sq = 0 if thickness == 0 else max(r - thickness, 0) ** 2

    # Coordinate grid
    yy, xx = np.mgrid[y0:y1, x0:x1]
    dx = xx - x
    dy = yy - y
    dist_sq = dx*dx + dy*dy

    mask = (radius_inner_sq <= dist_sq) & (dist_sq <= radius_outer_sq)
    sub = arr[y0:y1, x0:x1]
    sub[mask] = col


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
    sub = arr[y_min:y_max, x_min:x_max]
    sub[mask] = col
