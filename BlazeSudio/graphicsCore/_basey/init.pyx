# cython: boundscheck=False, wraparound=False, cdivision=True, initializedcheck=False
import numpy as np
class Base:
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

    def _warpbbx(self, mat, crop):
        topL = crop[:2]
        botR = (crop[2]-crop[0], crop[3]-crop[1])
        if self._regMat(mat):
            ps = self._regWarp(mat, topL), self._regWarp(mat, botR)
        else:
            ps = self._warpPs(mat, np.array([
                topL,
                [topL[0], botR[1]],
                botR,
                [botR[0], topL[1]]
            ], float))
        tl = (min(p[0] for p in ps),
              min(p[1] for p in ps))
        br = (max(p[0] for p in ps),
              max(p[1] for p in ps))
        if tl[0] >= br[0] or tl[1] >= br[1]:
            return None
        return (tl[0], tl[1], tl[0]+br[0], tl[1]+br[1])

