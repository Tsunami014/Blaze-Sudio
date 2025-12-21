# cython: boundscheck=False, wraparound=False, cdivision=True, initializedcheck=False
import numpy as np
cimport numpy as cnp
__cimport_types__ = [cnp.ndarray]

cdef cnp.ndarray[cnp.float64_t, ndim=2] invert_affine_matrix(mat):
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
        bint smooth):

    cdef long h = arr.shape[0]
    cdef long w = arr.shape[1]

    cdef bint persp
    cdef cnp.ndarray[cnp.float64_t, ndim=2] T_inv
    if mat[2,0] != 0 or mat[2,1] != 0:
        T_inv = np.linalg.inv(mat)
        persp = True
    else:
        T_inv = invert_affine_matrix(mat)
        persp = False
    cdef double[:, ::1] T = T_inv

    cdef unsigned char[:, :, ::1] in_arr = arr
    cdef cnp.ndarray[cnp.uint8_t, ndim=3] out = np.zeros((h, w, 4), dtype=np.uint8)
    cdef unsigned char[:, :, ::1] out_arr = out

    cdef double x, y
    cdef double z = 1
    cdef double sx, sy, wx, wy
    cdef long x0, y0

    cdef unsigned char *row0
    cdef long i, j, c
    if not smooth:
        for i in range(h):#, nogil=True):
            x = T[0,1] * i + T[0,2]
            y = T[1,1] * i + T[1,2]
            if persp: z = T[2,1] * i + T[2,2]
            for j in range(w):
                if z != 0:
                    if persp:
                        sx = x / z
                        sy = y / z
                        x0 = <long>sx
                        y0 = <long>sy
                    else:
                        x0 = <long>x
                        y0 = <long>y

                    row0 = &in_arr[y0, x0, 0]
                    if 0 <= x0 < w and 0 <= y0 < h:
                        out_arr[i, j, 0] = row0[0]
                        out_arr[i, j, 1] = row0[1]
                        out_arr[i, j, 2] = row0[2]
                        out_arr[i, j, 3] = row0[3]
                x = x + T[0,0]
                y = y + T[1,0]
                if persp: z = z + T[2,0]
        return out

    cdef unsigned char *row1
    cdef double top, bottom, val
    for i in range(h):#, nogil=True):
        x = T[0,1] * i + T[0,2]
        y = T[1,1] * i + T[1,2]
        if persp: z = T[2,1] * i + T[2,2]
        for j in range(w):
            if z != 0:
                if persp:
                    sx = x / z
                    sy = y / z
                    x0 = <long>sx
                    y0 = <long>sy
                else:
                    x0 = <long>x
                    y0 = <long>y

                if not (x0 < 0 or x0 + 1 >= w or y0 < 0 or y0 + 1 >= h):
                    if persp:
                        wx = sx - x0
                        wy = sy - y0
                    else:
                        wx = x - x0
                        wy = y - y0

                    row0 = &in_arr[y0, x0, 0]
                    row1 = &in_arr[y0 + 1, x0, 0]
                    for c in range(4):
                        top = (1 - wx) * row0[c] + wx * row0[4 + c]
                        bottom = (1 - wx) * row1[c] + wx * row1[4 + c]
                        out_arr[i,j,c] = <unsigned char>((1 - wy) * top + wy * bottom)
            x = x + T[0,0]
            y = y + T[1,0]
            if persp: z = z + T[2,0]
    return out


def blit(
        cnp.ndarray[cnp.float64_t, ndim=2] mat,
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
    tc = (mat @ corners.T).T
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

    cdef bint persp
    cdef cnp.ndarray[cnp.float64_t, ndim=2] Minv_
    if mat[2,0] != 0 or mat[2,1] != 0:
        Minv_ = np.linalg.inv(mat)
        persp = True
    else:
        Minv_ = invert_affine_matrix(mat)
        persp = False
    cdef double[:, ::1] Minv = Minv_
    cdef unsigned char[:, :, ::1] src_mv = src
    cdef unsigned char[:, :, ::1] dst_mv = dst

    cdef long x, y, ix, iy
    cdef double z = 1
    cdef double sx, sy, a, inv, oa
    cdef unsigned char sa
    cdef unsigned char *srcrow
    cdef unsigned char *dstrow
    for y in range(ymin, ymax):
        sx = Minv[0,0]*xmin + Minv[0, 1]*y + Minv[0, 2]
        sy = Minv[1,0]*xmin + Minv[1, 1]*y + Minv[1, 2]
        if persp: z = Minv[2,0]*xmin + Minv[2,1]*y + Minv[2,2]
        for x in range(xmin, xmax):#, nogil=True):
            if z != 0:
                if persp:
                    ix = <long>(sx / z)
                    iy = <long>(sy / z)
                else:
                    ix = <long>sx
                    iy = <long>sy

                if not (ix < 0 or iy < 0 or ix >= ow or iy >= oh):
                    sa = src[iy, ix, 3]
                    if sa != 0:
                        a = sa / 255.0
                        inv = 1.0 - a

                        srcrow = &src_mv[iy, ix, 0]
                        dstrow = &dst_mv[y, x, 0]

                        dstrow[0] = <unsigned char>(srcrow[0]*a + dstrow[0]*inv)
                        dstrow[1] = <unsigned char>(srcrow[1]*a + dstrow[1]*inv)
                        dstrow[2] = <unsigned char>(srcrow[2]*a + dstrow[2]*inv)
                        oa = sa + dstrow[3]*inv
                        if oa > 255:
                            oa = 255
                        dstrow[3] = <unsigned char>(oa)
            sx = sx + Minv[0, 0]
            sy = sy + Minv[1, 0]
            if persp: z = z + Minv[2,0]


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

