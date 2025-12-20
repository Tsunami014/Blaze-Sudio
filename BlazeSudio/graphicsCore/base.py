from . import _basey
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
], float)

class OpFlags(IntEnum):
    """
    Flags that make Operations act differently.
    Only for manual use if you know what you're doing.
    """
    NoFlags = 0
    """Has no flags. Is not special"""
    List = 0b1
    """Is an OpList"""
    Matrix = 0b10
    """Is a matrix operation"""
    StackMatrix = 0b110
    """Is a stackable matrix operation. These get stacked with other matrix operations"""
    DynMatrix = 0b1010
    """Is a dynamic matrix operation. These change their matrix based on the image"""
    Transformable = 0b10000
    """Is a transformable op. These get modified by future matrix operations"""
    Reset = 0b100000
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

class TransOp(_basey.TransBase, Op):
    def __init__(self):
        self.flags = OpFlags.Transformable

    def apply(self, arr, _):
        return self.applyTrans(IDENTITY, arr)
    @abstractmethod
    def applyTrans(self, mat: np.ndarray, arr: np.ndarray) -> np.ndarray: ...

class MatOp(Op):
    __slots__ = ['mat', '_smooth', '_centre']

    def __init__(self, mat, centre = True, smooth = None):
        self._smooth = smooth
        self._centre = centre
        self.mat = np.array(mat, float)
        if centre:
            self.flags = OpFlags.DynMatrix
        else:
            self.flags = OpFlags.StackMatrix

    def centredMat(self, arr: np.ndarray) -> np.ndarray:
        h, w, _ = arr.shape
        cx, cy = w/2, h/2
        T1 = np.array([[1, 0, -cx],[0, 1, -cy],[0, 0, 1]], float)
        T2 = np.array([[1, 0, cx], [0, 1, cy], [0, 0, 1]], float)
        return T2 @ self.mat @ T1

    def stack(self, nxt: 'MatOp'):
        if nxt._smooth is not None:
            smth = nxt._smooth
        else:
            smth = self._smooth
        return MatOp(self.mat @ nxt.mat, smth)

    def apply(self, arr: np.ndarray, defSmth: bool):
        smooth = self._smooth if self._smooth is not None else defSmth
        if self._centre:
            return _basey.apply(self.centredMat(arr), arr, smooth)
        else:
            return _basey.apply(self.mat, arr, smooth)

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
                    o.flags & nxt.flags & OpFlags.StackMatrix and \
                    o._smooth is not False:
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
        mat = IDENTITY
        skips = set()
        for idx, op in enumerate(self.ops):
            if op == nxtMat:
                nxtMat = None
                continue
            elif op in skips:
                continue
            if nxtMat is None:
                for i in range(idx, len(self.ops)):
                    o = self.ops[i]
                    if o.flags & OpFlags.Matrix:
                        nxtMat = o
                        if o.flags & OpFlags.StackMatrix:
                            mat = o.mat
                        else:
                            mat = o.getRealMat(arr.shape[1], arr.shape[0])
                        if o._smooth is not False:
                            for j in range(i+1, len(self.ops)):
                                o2 = self.ops[j]
                                if o2.flags & OpFlags.Matrix:
                                    if o.flags & OpFlags.StackMatrix:
                                        mat @= o.mat
                                    else:
                                        mat += o._grm(arr)
                                    skips.add(o2)
                                    if o2._smooth is False:
                                        break
                                else:
                                    break
                        # Apply the matrix here because all ops between now and the matrix will be transformed by themself
                        smooth = o._smooth if o._smooth is not None else defSmth
                        arr = _basey.apply(mat, arr, smooth)
                    # If it isn't transformable, don't keep finding the matrix
                    elif not o.flags & OpFlags.Transformable:
                        nxtMat = o
                        mat = IDENTITY
                        break
            if op.flags & OpFlags.Transformable:
                arr = op.applyTrans(mat, arr)
            arr = op.apply(arr, defSmth)
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

