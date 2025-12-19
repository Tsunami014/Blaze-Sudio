import numpy as np
cimport numpy as cnp
__cimport_types__ = [cnp.ndarray]

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

class TransBase:
    def _warpPs(self, mat: np.ndarray, points: np.ndarray):
        if self._regMat(mat):
            return points.astype(float) @ mat[:2, :2].T + mat[:2, 2]
        p = np.c_[points, np.ones(len(points))] @ mat.T
        return p[:, :2] / p[:, 2:3]

    def _regMat(self, mat: np.ndarray):
        """Returns True if a matrix is 'regular' - no rotations or perspective warps"""
        return mat[2, 0] == 0 and mat[2, 1] == 0 and mat[2, 2] == 1 and \
            (mat[0,1] == 0 and mat[1,0] == 0) or (mat[0,1] == 0 and mat[0,1] == [0, 0])

    def _regWarp(self, mat: np.ndarray, p):
        """Warps a point assuming no perspective warp (bottom row is [0, 0, 1])"""
        return np.array([
            p[0]*mat[0, 0] + p[1]*mat[1, 0] + mat[2, 0],
            p[0]*mat[0, 1] + p[1]*mat[1, 1] + mat[2, 1]
        ], dtype=float)

