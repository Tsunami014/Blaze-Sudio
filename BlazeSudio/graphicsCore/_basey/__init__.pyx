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


cdef inline void ezblit(
        const unsigned char[:, :, ::1] src_mv,
        unsigned char[:, :, ::1] dst_mv,
        long ow, long oh,
        long cLeft, long cTop, long cRight, long cBot,
        double scalex, double scaley, long transx, long transy
        ) noexcept nogil:
    cdef long x, y, ox, oy, oa
    cdef unsigned char sa, inva
    cdef const unsigned char *srcrow
    cdef unsigned char *dstrow
    if scalex == 1 and scaley == 1:
        for y in range(cTop, cBot):#, nogil=True):
            oy = y - transy
            if 0 <= oy < oh:
                for x in range(cLeft, cRight):
                    ox = x - transx
                    if 0 <= ox < ow:
                        srcrow = &src_mv[oy, ox, 0]
                        sa = srcrow[3]
                        if sa != 0:
                            inva = 255 - sa
                            dstrow = &dst_mv[y, x, 0]

                            dstrow[0] = <unsigned char>((srcrow[0]*sa + dstrow[0]*inva) >> 8)
                            dstrow[1] = <unsigned char>((srcrow[1]*sa + dstrow[1]*inva) >> 8)
                            dstrow[2] = <unsigned char>((srcrow[2]*sa + dstrow[2]*inva) >> 8)
                            oa = sa + dstrow[3]
                            if oa > 255:
                                oa = 255
                            dstrow[3] = <unsigned char>(oa)
        return

    for y in range(cTop, cBot):#, nogil=True):
        oy = <long>((y - transy) / scaley)
        if 0 <= oy < oh:
            for x in range(cLeft, cRight):
                ox = <long>((x - transx) / scalex)
                if 0 <= ox < ow:
                    srcrow = &src_mv[oy, ox, 0]
                    sa = srcrow[3]
                    if sa != 0:
                        inva = 255 - sa
                        dstrow = &dst_mv[y, x, 0]

                        dstrow[0] = <unsigned char>((srcrow[0]*sa + dstrow[0]*inva) >> 8)
                        dstrow[1] = <unsigned char>((srcrow[1]*sa + dstrow[1]*inva) >> 8)
                        dstrow[2] = <unsigned char>((srcrow[2]*sa + dstrow[2]*inva) >> 8)
                        oa = sa + dstrow[3]
                        if oa > 255:
                            oa = 255
                        dstrow[3] = <unsigned char>(oa)

def blit(
        cnp.ndarray[cnp.float64_t, ndim=2] mat,
        cnp.ndarray[cnp.uint8_t, ndim=3] src,
        cnp.ndarray[cnp.uint8_t, ndim=3] dst,
        crop):
    cdef long oh = src.shape[0]
    cdef long ow = src.shape[1]

    cdef double[:, ::1] mat_mv = mat
    cdef const unsigned char[:, :, ::1] src_mv = src
    cdef unsigned char[:, :, ::1] dst_mv = dst

    cdef long cLeft = <long>crop[0]
    cdef long cTop = <long>crop[1]
    cdef long cRight = <long>crop[2]
    cdef long cBot = <long>crop[3]

    cdef bint persp = mat_mv[2,0] != 0 or mat_mv[2,1] != 0 or mat_mv[2,2] != 1
    if (not persp) and mat_mv[0,1] == 0 and mat_mv[1,0] == 0:
        ezblit(
            src_mv, dst_mv,
            ow, oh, cLeft, cTop, cRight, cBot,
            mat_mv[0,0], mat_mv[1,1], <long>mat_mv[0,2], <long>mat_mv[1,2])
        return

    cdef cnp.ndarray[cnp.float64_t, ndim=2] Minv_
    if persp:
        Minv_ = np.linalg.inv(mat)
    else:
        Minv_ = invert_affine_matrix(mat)
    cdef double[:, ::1] Minv = Minv_

    cdef long x, y, ox, oy, oa
    cdef double z = 1
    cdef double sx, sy
    cdef unsigned char sa, inva
    cdef const unsigned char *srcrow
    cdef unsigned char *dstrow
    for y in range(cTop, cBot):#, nogil=True):
        sx = Minv[0,0]*cLeft + Minv[0, 1]*y + Minv[0, 2]
        sy = Minv[1,0]*cLeft + Minv[1, 1]*y + Minv[1, 2]
        if persp: z = Minv[2,0]*cLeft + Minv[2,1]*y + Minv[2,2]
        for x in range(cLeft, cRight):
            if z != 0:
                if persp:
                    ox = <long>(sx / z)
                    oy = <long>(sy / z)
                else:
                    ox = <long>sx
                    oy = <long>sy

                if 0 <= ox < ow and 0 <= oy < oh:
                    srcrow = &src_mv[oy, ox, 0]
                    sa = srcrow[3]
                    if sa != 0:
                        inva = 255 - sa
                        dstrow = &dst_mv[y, x, 0]

                        dstrow[0] = <unsigned char>((srcrow[0]*sa + dstrow[0]*inva) >> 8)
                        dstrow[1] = <unsigned char>((srcrow[1]*sa + dstrow[1]*inva) >> 8)
                        dstrow[2] = <unsigned char>((srcrow[2]*sa + dstrow[2]*inva) >> 8)
                        oa = sa + dstrow[3]
                        if oa > 255:
                            oa = 255
                        dstrow[3] = <unsigned char>(oa)
            sx = sx + Minv[0, 0]
            sy = sy + Minv[1, 0]
            if persp: z = z + Minv[2,0]


class TransBase:
    def _warpPs(self, mat: np.ndarray, points: np.ndarray):
        points = points.astype(float)
        if self._affMat(mat):
            return points @ mat[:2, :2].T + mat[:2, 2]
        p = np.c_[points, np.ones(len(points))] @ mat.T
        return p[:, :2] / p[:, 2:3]

    def _regMat(self, mat: np.ndarray):
        """Returns True if a matrix is 'regular' - no rotations or perspective warps"""
        return (
            mat[2, 0] == 0 and mat[2, 1] == 0 and mat[2, 2] == 1 and
            (
                (mat[0,1] == 0 and mat[1,0] == 0) or
                (mat[0,1] == 0 and mat[0,1] == [0, 0])
            )
        )
    def _affMat(self, mat: np.ndarray):
        """Returns True if a matrix is 'affine' - no perspective warps"""
        return mat[2, 0] == 0 and mat[2, 1] == 0 and mat[2, 2] == 1

    def _regWarp(self, mat: np.ndarray, p, offset: bool = True):
        """Warps a point assuming no perspective warp (bottom row is [0, 0, 1])"""
        cdef float x = p[0]
        cdef float y = p[1]
        if offset:
            return np.array([
                x*mat[0, 0] + y*mat[0, 1] + mat[0, 2],
                x*mat[1, 0] + y*mat[1, 1] + mat[1, 2]
            ], dtype=float)
        else:
            return np.array([
                x*mat[0, 0] + y*mat[0, 1],
                x*mat[1, 0] + y*mat[1, 1]
            ], dtype=float)

