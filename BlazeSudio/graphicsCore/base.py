from . import _calcs
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
    NoFlags = 0
    """Has no flags. Is not special."""
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
    __slots__ = ['flags']

    @abstractmethod
    def __init__(self): ...
    @abstractmethod
    def apply(self, arr: np.ndarray, defSmth: bool) -> np.ndarray: ...

    def freeze(self):
        self.flags = OpFlags.NoFlags # It is no longer a whatever and unable to be stacked
    def frozen(self) -> 'Op':
        self.flags = OpFlags.NoFlags
        return self

    def __add__(self, oth) -> 'OpList':
        if oth.flags & OpFlags.List:
            return OpList(self, *oth.ops)
        return OpList(self, oth)

    def flatten(self):
        return self

class TransOp(Op):
    def __init__(self):
        self.flags = OpFlags.Transformable

    def _warpPs(self, mat, points):
        p = np.c_[points, np.ones(len(points))] @ mat.T
        return p[:, :2] / p[:, 2:3]

    def apply(self, arr, _):
        return self.applyTrans(IDENTITY, arr)
    @abstractmethod
    def applyTrans(self, mat: np.ndarray, arr: np.ndarray) -> np.ndarray: ...

class MatOp(Op):
    __slots__ = ['mat', '_smooth']

    def __init__(self, mat, smooth = None):
        self.mat = np.ndarray(mat, np.int64)
        self._smooth = smooth
        self.flags = OpFlags.Matrix

    def stack(self, nxt: 'MatOp'):
        if self._smooth is not None:
            smth = self._smooth
        else:
            smth = nxt._smooth
        return MatOp(self.mat @ nxt.mat, smth)

    def apply(self, arr: np.ndarray, defSmth: bool):
        smooth = self._smooth if self._smooth is not None else defSmth
        _calcs.apply(self.mat, arr, smooth)

class OpList(Op):
    __slots__ = ['ops', '_fixed', 'flags']
    def __init__(self, *ops):
        self.ops = ops
        self._fixed = False
        self.flags = OpFlags.List

    def fix(self):
        if self._fixed:
            return
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
        self._fixed = True

    def freeze(self):
        if not self._fixed:
            self.fix()
        self.flags = OpFlags.NoFlags
    def frozen(self) -> 'Op':
        if not self._fixed:
            self.fix()
        self.flags = OpFlags.NoFlags
        return self

    def apply(self, arr: np.ndarray, defSmth):
        if not self._fixed:
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
        if not self.flags & OpFlags.List:
            if oth.flags & OpFlags.List:
                return OpList(self, *oth.ops)
            return OpList(self, oth)
        if oth.flags & OpFlags.List:
            return OpList(*self.ops, *oth.ops)
        return OpList(*self.ops, oth)

    def flatten(self):
        return self.ops

