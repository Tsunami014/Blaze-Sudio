# cython: boundscheck=False, wraparound=False, cdivision=True
import numpy as np
cimport numpy as cnp
from libc.math cimport floor
__cimport_types__ = [cnp.ndarray, floor]

cdef cnp.ndarray[cnp.float64_t, ndim=2] invert_matrix(mat):
    if mat[2,0] != 0 or mat[2,1] != 0:
        return np.linalg.inv(mat)

    cdef double a, b, tx
    cdef double c, d, ty
    a, b, tx = mat[0]
    c, d, ty = mat[1]
    cdef double det = a*d - b*c
    if det == 0:
        raise ValueError("Singular affine")
    return np.array([
        [ d/det, -b/det, (b*ty - d*tx)/det ],
        [-c/det,  a/det, (c*tx - a*ty)/det ],
        [ 0, 0, 1 ]
    ], dtype=np.float64)

def apply(
        cnp.ndarray[cnp.float64_t, ndim=2] mat,
        cnp.ndarray[cnp.uint8_t, ndim=3] arr,
        bool smooth):

    cdef long h = arr.shape[0]
    cdef long w = arr.shape[1]
    cdef long ch = arr.shape[2]
    cdef long i, j, c

    cdef T_inv = invert_matrix(mat)
    cdef double[:, ::1] T = T_inv

    cdef double x, y, z
    cdef double sx, sy, wx, wy
    cdef long x0, y0

    cdef double top, bottom, val
    cdef unsigned char[:, :, ::1] in_arr = arr
    cdef cnp.ndarray[cnp.uint8_t, ndim=3] out = np.zeros((h, w, ch), dtype=np.uint8)
    cdef unsigned char[:, :, ::1] out_arr = out

    if smooth:
        for i in range(h):
            x = T[0,1] * i + T[0,2]
            y = T[1,1] * i + T[1,2]
            z = T[2,1] * i + T[2,2]
            for j in range(w):
                if z != 0:
                    sx = x / z
                    sy = y / z

                    x0 = <long>floor(sx)
                    y0 = <long>floor(sy)

                    if not (x0 < 0 or x0 + 1 >= w or y0 < 0 or y0 + 1 >= h):
                        wx = sx - x0
                        wy = sy - y0

                        for c in range(ch):
                            top = (1 - wx) * in_arr[y0, x0, c] + wx * in_arr[y0, x0 + 1, c]
                            bottom = (1 - wx) * in_arr[y0 + 1, x0, c] + wx * in_arr[y0 + 1, x0 + 1, c]
                            out_arr[i, j, c] = <unsigned char>((1 - wy) * top + wy * bottom)
                x += T[0,0]
                y += T[1,0]
                z += T[2,0]
        return out
    else:
        for i in range(h):
            x = T[0,1] * i + T[0,2]
            y = T[1,1] * i + T[1,2]
            z = T[2,1] * i + T[2,2]
            for j in range(w):
                if z != 0:
                    sx = x / z
                    sy = y / z

                    x0 = <long>floor(sx)
                    y0 = <long>floor(sy)

                    if 0 <= x0 < w and 0 <= y0 < h:
                        for c in range(ch):
                            out_arr[i, j, c] = in_arr[y0, x0, c]
                x += T[0,0]
                x += T[1,0]
                x += T[2,0]

        return out


def blit(
        cnp.ndarray[cnp.float64_t, ndim=2] M,
        cnp.ndarray[cnp.uint8_t, ndim=3] src,
        cnp.ndarray[cnp.uint8_t, ndim=3] dst):
    cdef long oh = src.shape[0]
    cdef long ow = src.shape[1]
    cdef long dh = dst.shape[0]
    cdef long dw = dst.shape[1]
    cdef cnp.ndarray[cnp.float32_t, ndim=2] corners = np.array([
        [0,  0,  1],
        [ow, 0,  1],
        [ow, oh, 1],
        [0,  oh, 1],
    ], dtype=np.float32)
    tc = (M @ corners.T).T
    xs = tc[:, 0]
    ys = tc[:, 1]

    cdef long xmin = <long>xs.min()
    if xmin < 0:
        xmin = 0
    cdef long xmax = <long>xs.max() + 1
    if xmax > dw:
        xmax = dw
    cdef long ymin = <long>ys.min()
    if ymin < 0:
        ymin = 0
    cdef long ymax = <long>ys.max() + 1
    if ymax > dh:
        ymax = dh

    cdef cnp.ndarray[cnp.float64_t, ndim=2] Minv = invert_matrix(M)
    cdef long y, x, ix, iy
    cdef double sx, sy, a, inv
    cdef unsigned char sa, oa
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            sx = Minv[0, 0]*x + Minv[0, 1]*y + Minv[0, 2]
            sy = Minv[1, 0]*x + Minv[1, 1]*y + Minv[1, 2]

            ix = <long>sx
            iy = <long>sy

            if ix < 0 or iy < 0 or ix >= ow or iy >= oh:
                continue

            sa = src[iy, ix, 3]
            if sa == 0:
                continue

            a = sa / 255.0
            inv = 1.0 - a

            dst[y, x, 0] = <unsigned char>(src[iy, ix, 0]*a + dst[y, x, 0]*inv)
            dst[y, x, 1] = <unsigned char>(src[iy, ix, 1]*a + dst[y, x, 1]*inv)
            dst[y, x, 2] = <unsigned char>(src[iy, ix, 2]*a + dst[y, x, 2]*inv)
            oa = <unsigned char>(sa + dst[y, x, 3]*inv)
            if oa > 255:
                oa = 255
            dst[y, x, 3] = oa


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

