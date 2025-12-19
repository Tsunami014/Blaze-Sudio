# cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True
import numpy as np
cimport numpy as cnp
__cimport_types__ = [cnp.ndarray]


def drawLine(
        cnp.ndarray[cnp.uint8_t, ndim=3] arr,
        double[:] p1,
        double[:] p2,
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

def drawPolyLine(
        cnp.ndarray[cnp.uint8_t, ndim=3] arr,
        double[:, :] points,
        double thickness,
        cnp.ndarray[cnp.uint8_t, ndim=1] col,
        bool round):
    cdef long ht = <long>(thickness // 2)
    cdef long n = len(points)
    if round:
        for i in range(n):
            drawCirc(arr, points[i], ht, 0, col)
    if n == 2:
        drawLine(arr, points[0], points[1], thickness, col)
        return
    p1 = points[0]
    for i in range(1, n):
        p2 = points[i]
        drawLine(arr, p1, p2, thickness, col)
        p1 = p2
    drawLine(arr, p1, points[0], thickness, col)


cdef inline long _clip(long v, long lo, long hi):
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v

def drawRect(
        cnp.ndarray[cnp.uint8_t, ndim=3] arr,
        double[:] pos,
        double[:] sze,
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


def drawCirc(
        cnp.ndarray[cnp.uint8_t, ndim=3] arr,
        double[:] pos,
        double radius,
        double thickness,
        cnp.ndarray[cnp.uint8_t, ndim=1] col):
    cdef long r = <long>radius
    cdef long w = <long>arr.shape[1]
    cdef long h = <long>arr.shape[0]
    cdef long x = <long>pos[0]
    cdef long y = <long>pos[1]

    cdef long y0 = max(y - r - 1, 0)
    cdef long y1 = min(y + r + 1, h)
    cdef long x0 = max(x - r - 1, 0)
    cdef long x1 = min(x + r + 1, w)
    if y0 >= y1 or x0 >= x1:
        return

    cdef long outrad2 = r * r
    cdef long innrad2
    if thickness == 0:
        innrad2 = 0
    else:
        innrad2 = max(r - <long>thickness, 0)
        innrad2 *= innrad2

    cdef long xx, yy
    cdef long dx, dy
    cdef long dist_sq
    for yy in range(y0, y1):
        dy = yy - y
        for xx in range(x0, x1):
            dx = xx - x
            dist_sq = dx*dx + dy*dy

            if innrad2 <= dist_sq <= outrad2:
                arr[yy, xx, :] = col


def drawElipse(
        cnp.ndarray[cnp.uint8_t, ndim=3] arr,
        double[:] pos,
        double xradius,
        double yradius,
        double rotation,
        double thickness,
        cnp.ndarray[cnp.uint8_t, ndim=1] col):
    cdef long xrad = <long>xradius
    cdef long yrad = <long>yradius
    cdef long w = <long>arr.shape[1]
    cdef long h = <long>arr.shape[0]
    cdef long x = <long>pos[0]
    cdef long y = <long>pos[1]

    cdef long t
    if thickness >= min(xrad, yrad):
        t = 0
    else:
        t = <long>(thickness / 2)

    # Bounding box
    cdef long x_min = max(x - xrad- 1 - t, 0)
    cdef long x_max = min(x + xrad+ 1 + t, w)
    cdef long y_min = max(y - yrad- 1 - t, 0)
    cdef long y_max = min(y + yrad+ 1 + t, h)

    # Rotation
    cdef double cos_t = np.cos(rotation)
    cdef double sin_t = np.sin(rotation)

    cdef long xx, yy
    cdef double dx, dy
    cdef double xr, yr
    cdef double v_outer, v_inner

    if t == 0:
        invxr = 1.0 / (xrad * xrad)
        invyr = 1.0 / (yrad * yrad)
        for yy in range(y_min, y_max):
            dy = yy - y
            for xx in range(x_min, x_max):
                dx = xx - x

                xr = dx * cos_t + dy * sin_t
                yr = -dx * sin_t + dy * cos_t

                if xr * xr * invxr + yr * yr * invyr <= 1.0:
                    arr[yy, xx, :] = col
    else:
        inv_right = 1.0 / ((xrad + t) * (xrad + t))
        inv_bot = 1.0 / ((yrad + t) * (yrad + t))
        inv_left = 1.0 / ((xrad - t) * (xrad - t))
        inv_right = 1.0 / ((yrad - t) * (yrad - t))

        for yy in range(y_min, y_max):
            dy = yy - y
            for xx in range(x_min, x_max):
                dx = xx - x

                xr = dx * cos_t + dy * sin_t
                yr = -dx * sin_t + dy * cos_t

                v_outer = xr * xr * inv_right + yr * yr * inv_bot
                if v_outer <= 1.0:
                    v_inner = xr * xr * inv_left + yr * yr * inv_right
                    if v_inner > 1.0:
                        arr[yy, xx, :] = col

