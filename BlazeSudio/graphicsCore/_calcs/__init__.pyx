# cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True
import numpy as np


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

def _drawRoundThickLine(
        arr,
        double[:] p1,
        double[:] p2,
        double thickness,
        colour):
    cdef long x = <long>p1[0]
    cdef long y = <long>p1[1]
    cdef long x1 = <long>p2[0]
    cdef long y1 = <long>p2[1]
    cdef int radius = int(thickness) >> 1
    if radius < 0:
        radius = 0

    # precompute circle mask for this call
    gy, gx = np.ogrid[-radius:radius+1, -radius:radius+1]
    mask = (gx*gx + gy*gy) <= radius*radius
    offs_y, offs_x = np.nonzero(mask)
    offs_y -= radius
    offs_x -= radius

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
            y0 = max(y - radius, 0)
            y1b = min(y + radius + 1, h)
            x0 = max(x - radius, 0)
            x1b = min(x + radius + 1, w)

            my0 = y0 - (y - radius)
            mx0 = x0 - (x - radius)
            my1 = my0 + (y1b - y0)
            mx1 = mx0 + (x1b - x0)

            submask = mask[my0:my1, mx0:mx1]
            if submask.size:
                sub = arr[y0:y1b, x0:x1b]
                sub[submask] = colour

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
            y0 = max(y - radius, 0)
            y1b = min(y + radius + 1, h)
            x0 = max(x - radius, 0)
            x1b = min(x + radius + 1, w)

            my0 = y0 - (y - radius)
            mx0 = x0 - (x - radius)
            my1 = my0 + (y1b - y0)
            mx1 = mx0 + (x1b - x0)

            submask = mask[my0:my1, mx0:mx1]
            if submask.size:
                sub = arr[y0:y1b, x0:x1b]
                sub[submask] = colour

            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += 1

def _drawThickLine(
        arr,
        double[:] p1,
        double[:] p2,
        double thickness,
        colour):
    cdef long x = <long>p1[0]
    cdef long y = <long>p1[1]
    cdef long x1 = <long>p2[0]
    cdef long y1 = <long>p2[1]

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
            y0 = max(y, 0)
            y1b = min(y + 1, h)
            x0 = max(x, 0)
            x1b = min(x + 1, w)

            my1 = (y0 - y) + (y1b - y0)
            mx1 = (x0 - x) + (x1b - x0)

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
            x0 = max(x, 0)
            x1b = min(x + 1, w)

            my1 = (y0 - y) + (y1b - y0)
            mx1 = (x0 - x) + (x1b - x0)

            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += 1


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
            sub = arr[ys:ye, xs:xe]
            sub[mask] = col


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
    sub = arr[rng]
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
