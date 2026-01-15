import numpy as np

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

