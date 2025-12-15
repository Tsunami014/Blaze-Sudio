from abc import ABC, abstractmethod
from enum import IntEnum
import numpy as np

__all__ = [
    'OpFlags',
    'Op',
        'TransOp',
        'MatOp',
    'OpList'
]

IDENTITY = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
], np.int64)

class OpFlags(IntEnum):
    """
    Flags that make Operations act differently.
    Only for manual use if you know what you're doing.
    """
    List = 0b1
    """Is an OpList"""
    Matrix = 0b10
    """Is a matrix operation. These get stacked with other matrix operations"""
    Transformable = 0b100
    """Is a transformable op. These get modified by future matrix operations"""
    Reset = 0b1000
    """Is a reset op. Every op before it will be ignored"""

class Op(ABC):
    """Please, wherever possible, use TransOps instead. It's faster."""
    __slots__ = []
    flags: int = 0

    @abstractmethod
    def __init__(self): ...
    @abstractmethod
    def apply(self, arr: np.ndarray, defSmth: bool) -> np.ndarray: ...

    def __add__(self, oth) -> 'OpList':
        if oth.flags & OpFlags.List:
            return OpList(self, *oth.ops)
        return OpList(self, oth)

class TransOp(Op):
    flags = OpFlags.Transformable

    def _warpPs(self, mat, points):
        p = np.c_[points, np.ones(len(points))] @ mat.T
        return p[:, :2] / p[:, 2:3]

    def apply(self, arr, _):
        return self.applyTrans(IDENTITY, arr)
    @abstractmethod
    def applyTrans(self, mat: np.ndarray, arr: np.ndarray) -> np.ndarray: ...

class MatOp(Op):
    __slots__ = ['mat', '_smooth']
    flags = OpFlags.Matrix

    def __init__(self, mat, smooth = None):
        self.mat = np.ndarray(mat, np.int64)
        self._smooth = smooth

    def stack(self, nxt: 'MatOp'):
        if self._smooth is not None:
            smth = self._smooth
        else:
            smth = nxt._smooth
        return MatOp(self.mat @ nxt.mat, smth)

    def apply(self, arr: np.ndarray, defSmth: bool):
        smooth = self._smooth if self._smooth is not None else defSmth
        background = 0

        h, w = arr.shape[:2]
        is_color = arr.ndim == 3

        T_inv = np.linalg.inv(self.mat)

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

class OpList(Op):
    __slots__ = ['ops', 'fixed', 'flags']
    def __init__(self, *ops):
        self.ops = ops
        self.fixed = False
        self.flags = ops[-1].flags | OpFlags.List

    def fix(self):
        ops = self.ops
        self.ops = []
        it = iter(ops)
        o = next(it, None)
        while o is not None:
            o2 = o
            while (nxt := next(it, None)) is not None and \
                     o.flags & nxt.flags & OpFlags.Matrix and \
                    (o._smooth is None or nxt._smooth is None or o._smooth == nxt._smooth):
                o2 = o.stack(nxt)
                o = nxt
            self.ops.append(o2)
            o = nxt

    def apply(self, arr: np.ndarray, defSmth):
        if not self.fixed:
            self.fix() # Lazily fix it so it won't every new addition
        nxtMat = None
        mat = None
        for idx, op in enumerate(self.ops):
            if nxtMat is None:
                for i in range(idx, len(self.ops)):
                    o = self.ops[i]
                    if o.flags & OpFlags.Matrix:
                        nxtMat = o
                        mat = o.mat
                        # Apply the matrix here because all ops between now and the matrix are already transformed
                        arr = o.apply(arr, defSmth)
                        break
                    # If it isn't transformable, don't keep finding the matrix
                    elif not o.flags & OpFlags.Transformable:
                        nxtMat = o
                        mat = IDENTITY
                        break
            if op.flags & OpFlags.Transformable:
                arr = op.applyTrans(mat, arr)
            elif not op.flags & OpFlags.Matrix: # We already apply the matrix ops earlier
                arr = op.apply(arr, defSmth)

            if op == nxtMat:
                nxtMat = None
        return arr

    def __add__(self, oth) -> 'OpList':
        if oth.flags & OpFlags.List:
            return OpList(*self.ops, *oth.ops)
        return OpList(*self.ops, oth)

