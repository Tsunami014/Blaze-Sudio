from . import _basey
from ._vec2 import Vec2 as _v2
from typing import Self
from abc import ABC, abstractmethod
from enum import IntEnum
import numpy as np

__all__ = [
    'Anchors',
    'IDENTITY',
    'OpFlags',
    'Vec2',
    'Op',
        'NormalisedOp',
        'OpList',
        'TransOp',
    'MatTrans'
]

class Anchors:
    _nx = 'normalise_x'
    _ny = 'normalise_y'
    TopLeft =  {_nx: 0,   _ny: 0}
    TopMid =   {_nx: 0.5, _ny: 0}
    TopRight = {_nx: 1,   _ny: 0}
    MidLeft =  {_nx: 0,   _ny: 0.5}
    Middle =   {_nx: 0.5, _ny: 0.5}
    MidMid =   Middle
    MidRight = {_nx: 1,   _ny: 0.5}
    BotLeft =  {_nx: 0,   _ny: 1}
    BotMid =   {_nx: 0.5, _ny: 1}
    BotRight = {_nx: 1,   _ny: 1}

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
    Normalised = 0b10
    """Is a NormalisedOp"""
    Reset = 0b100
    """Is a reset op. Every op before it will be ignored"""
    Matrix = 0b1000
    """Is a matrix operation"""


class Vec2(_v2):
    flags = OpFlags.Matrix

    @property
    def mat(self) -> np.ndarray:
        return np.array([
            [1, 0, self.pos[0]],
            [0, 1, self.pos[1]],
            [0, 0, 1]
        ], float)

class MatTrans:
    __slots__ = ['flags', 'mat']

    def __init__(self, mat):
        self.mat = np.array(mat, float)
        self.flags = OpFlags.Matrix

    def __add__(self, oth) -> 'MatTrans':
        if not isinstance(oth, (MatTrans, Vec2)):
            oth = Vec2(*oth)
        return MatTrans(oth.mat @ self.mat)


class Op(ABC, _basey.TransBase):
    __slots__ = ['flags']

    @abstractmethod
    def apply(self, mat: np.ndarray, arr: np.ndarray, defSmth: bool) -> np.ndarray: ...

    def frozen(self) -> Self:
        """Get the frozen verson of this operation"""
        return self
    def freeze(self) -> Self:
        """Freezes this operation and returns it"""
        return self

    def __add__(self, oth) -> 'OpList':
        if oth.flags & OpFlags.List:
            return OpList(self, *oth.ops)
        return OpList(self, oth)

    def __matmul__(self, oth) -> 'TransOp':
        if not isinstance(oth, (MatTrans, Vec2)):
            oth = Vec2(*oth)
        return TransOp(self.frozen(), oth)

    def __iter__(self):
        return iter((self,))
    def flatten(self):
        return self

class NormalisedOp(Op):
    __slots__ = []

    def __init__(self, *, normalise_x = None, normalise_y = None):
        self.flags = OpFlags.Normalised
        if normalise_x is not None and normalise_y is not None:
            ox, oy = self.getNormalisedPos(normalise_x, normalise_y)
            if normalise_x is None:
                ox = 0
            if normalise_y is None:
                oy = 0
            self._translate(-ox, -oy)

    @abstractmethod
    def rect(self):
        """Returns a tuple in the format (topleft_x, topleft_y, width, height)"""
    @abstractmethod
    def _translate(self, x, y): ...
    
    def getNormalisedPos(self, normalise_x: float = 0, normalise_y: float = 0):
        """Get the true position of a normalised point."""
        x, y, wid, hei = self.rect()
        return Vec2(x + wid * normalise_x, y + hei * normalise_y)

class OpList(Op):
    __slots__ = ['ops', '_fixed', 'flags']
    def __init__(self, *ops):
        self.ops = ops
        self._fixed = False
        self.flags = OpFlags.List

    def rect(self):
        """
        Get the rect (x, y, width, height) that surrounds all ops in this list.

        If any operation is not a NormalisedOp, will return (None, None, None, None)
        """
        if not self._fixed:
            self.fix()
        if not self.flags & OpFlags.Normalised:
            return None, None, None, None
        rs = [
            (x, y, x+w, y+h) for x, y, w, h in
                (o.rect() for o in self.ops)
        ]
        topLeft = [
            min(i[0] for i in rs),
            min(i[1] for i in rs),
        ]
        botRight = [
            max(i[2] for i in rs),
            max(i[3] for i in rs),
        ]
        return *topLeft, botRight[0]-topLeft[0], botRight[1]-topLeft[1]

    def getNormalisedPos(self, normalise_x: float = 0, normalise_y: float = 0):
        """
        Get the true position of a normalised point.

        If any operation is not a NormalisedOp, will return (None, None)
        """
        x, y, wid, hei = self.rect()
        if x is None:
            return None, None
        return x + wid * normalise_x, y + hei * normalise_y

    def _unpack(self, li):
        for it in li:
            if it.flags & OpFlags.List:
                yield from self._unpack(it)
            else:
                yield it

    def fix(self):
        if self._fixed:
            return
        ops = list(self._unpack(self.ops))
        for idx, o in enumerate(ops[::-1]):
            if o.flags & OpFlags.Reset:
                ops = ops[-1-idx:]
                break # We're going backwards
        self.ops = ops
        if any(i.flags & OpFlags.Reset for i in ops):
            self.flags |= OpFlags.Reset # Add the reset flag
        else:
            self.flags &= ~OpFlags.Reset # Remove the reset flag
        if all(i.flags & OpFlags.Normalised for i in ops):
            self.flags |= OpFlags.Normalised
        else:
            self.flags &= ~OpFlags.Normalised
        self._fixed = True

    def frozen(self) -> 'OpList':
        """Get an op list that is the frozen version of this"""
        if not self._fixed:
            self.fix()
        nl = OpList(*self.ops)
        nl._fixed = True # We did that just then, no need to do it twice
        nl.flags = self.flags & ~OpFlags.List # Every flag except List
        return nl
    def freeze(self) -> Self:
        """Freezes this op list and returns it"""
        if not self._fixed:
            self.fix()
        self.flags = self.flags & ~OpFlags.List
        return self

    def apply(self, mat: np.ndarray, arr: np.ndarray, defSmth):
        if not self._fixed:
            self.fix() # Lazily fix it so it won't every new addition
        for op in self.ops:
            arr = op.apply(mat, arr, defSmth)
        return arr

    def __add__(self, oth) -> 'OpList':
        if not self.flags & OpFlags.List:
            if oth.flags & OpFlags.List:
                return OpList(self, *oth.ops)
            return OpList(self, oth)
        if oth.flags & OpFlags.List:
            return OpList(*self.ops, *oth.ops)
        return OpList(*self.ops, oth)

    def __iter__(self):
        if not self._fixed:
            self.fix()
        return iter(self.ops)
    def flatten(self):
        if not self._fixed:
            self.fix()
        return self.ops

class TransOp(Op):
    __slots__ = ['op', 'trans']
    flags = OpFlags.NoFlags
    def __init__(self, op: Op, trans: MatTrans|None):
        self.op = op
        self.trans = trans

    def apply(self, mat: np.ndarray, arr: np.ndarray, defSmth):
        if self.trans is not None:
            return self.op.apply(mat @ self.trans.mat, arr, defSmth)
        else:
            return self.op.apply(mat, arr, defSmth)

    def frozen(self) -> 'OpList':
        return self.op.frozen()
    def freeze(self) -> 'OpList':
        return self.op.freeze()

    def __iter__(self):
        return iter(self.op)
    def flatten(self):
        return self.op

