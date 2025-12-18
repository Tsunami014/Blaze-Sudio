import numpy as np

def _drawThickLine(arr: np.ndarray, p1: np.ndarray, p2: np.ndarray, thickness: int, colour: np.ndarray):
    x, y = p1.astype(np.int64)
    x1, y1 = p2.astype(np.int64)
    radius = int(thickness) // 2

    # Precompute circle mask
    yy, xx = np.ogrid[-radius:radius+1, -radius:radius+1]
    circle_mask = xx*xx + yy*yy <= radius*radius
    offsets = np.arange(-radius, radius+1, dtype=np.int64)

    dx = abs(x1 - x)
    dy = abs(y1 - y)
    if dx > dy:
        if x > x1:
            x, x1 = x1, x
            y, y1 = y1, y
        sy = 1 if y < y1 else -1
        err = dx / 2
        while x <= x1:
            y0 = max(y - radius, 0)
            y1b = min(y + radius + 1, arr.shape[0])
            x0 = max(x - radius, 0)
            x1b = min(x + radius + 1, arr.shape[1])

            sub = arr[y0:y1b, x0:x1b]

            my0 = y0 - (y - radius)
            mx0 = x0 - (x - radius)
            my1 = my0 + (y1b - y0)
            mx1 = mx0 + (x1b - x0)

            sub[circle_mask[my0:my1, mx0:mx1]] = colour

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
            y0 = max(y - radius, 0)
            y1b = min(y + radius + 1, arr.shape[0])
            x0 = max(x - radius, 0)
            x1b = min(x + radius + 1, arr.shape[1])

            sub = arr[y0:y1b, x0:x1b]

            my0 = y0 - (y - radius)
            mx0 = x0 - (x - radius)
            my1 = my0 + (y1b - y0)
            mx1 = mx0 + (x1b - x0)

            sub[circle_mask[my0:my1, mx0:mx1]] = colour

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
