from .base import Op, NormalisedOp, OpFlags, Vec2, Trans, _basey
from .core import _SurfaceBase
from PIL import Image as _PillowImg
from typing import overload
import numpy as np

__all__ = [
    'Fill',
    'Crop',
    'Surf',
        'Image',
        'Preserve'
]

class Fill(Op):
    __slots__ = ['col']
    def __init__(self, col):
        self.col = np.array(col, np.uint8)
        self.flags = OpFlags.Reset
    def apply(self, _, arr: np.ndarray, __, ___):
        if (self.col[0] == self.col[1] == self.col[2]).all():
            arr.fill(self.col[0])
        else:
            arr[...] = self.col
        return arr


class Crop(Trans, _basey.TransBase):
    __slots__ = ['topL', 'botR']

    @overload
    def __init__(self,
            x: float, y: float, wid: float, hei: float,
            *, normalise_x = None, normalise_y = None):
        """Crop the sub-ops to the rect (x, y, wid, hei) (as a union with the parent crops)"""
    @overload
    def __init__(self, pos, sze,
            *, normalise_x = None, normalise_y = None):
        """Crop the sub-ops to the rect (pos, sze) (as a union with the parent crops)"""
    def __init__(self, *args, normalise_x = None, normalise_y = None):
        match len(args):
            case 2:
                r = [*args[0], *args[1]]
            case 4:
                r = list(args)
            case _:
                raise TypeError(
                    f'Incorrect number of arguments! Expected 2 or 4, found {len(args)}!'
                )
        self.topL = list(r[:2])
        if normalise_x is not None:
            self.topL[0] += r[2] * normalise_x
        if normalise_y is not None:
            self.topL[1] += r[3] * normalise_y
        self.botR = (r[2]+self.topL[0], r[3]+self.topL[1])

    @property
    def size(self):
        return self.botR[0]-self.topL[0], self.botR[1]-self.topL[1]
    @size.setter
    def size(self, new):
        self.botR = (
            self.topL[0] + new[0],
            self.topL[1] + new[1]
        )
    @property
    def pos(self):
        return self.topL
    @pos.setter
    def pos(self, new):
        osze = self.size
        self.topL = new
        self.botR = (new[0]+osze[0], new[1]+osze[1])

    @property
    def rect(self):
        return *self.topL, *self.size
    @rect.setter
    def rect(self, new):
        self.topL = new[:2]
        self.botR = (new[2]+new[0], new[3]+new[1])

    def apply(self, mat: np.ndarray, crop, defSmth: bool):
        if self._regMat(mat):
            ps = self._regWarp(mat, self.topL), self._regWarp(mat, self.botR)
        else:
            ps = self._warpPs(mat, np.array([
                self.topL,
                [self.topL[0], self.botR[1]],
                self.botR,
                [self.botR[0], self.topL[1]]
            ], float))
        tl = (min(p[0] for p in ps),
              min(p[1] for p in ps))
        br = (max(p[0] for p in ps),
              max(p[1] for p in ps))
        topLeft = (
            max(crop[0], tl[0]),
            max(crop[1], tl[1]),
        )
        botRight = (
            min(crop[2], br[0]),
            min(crop[3], br[1]),
        )
        if topLeft[0] >= botRight[0] or topLeft[1] >= botRight[1]:
            return None
        newR = (
            *topLeft, *botRight
        )
        return mat, newR, defSmth


class _SurfaceBase2(NormalisedOp):
    """Must define _sze and arr in subclass"""
    __slots__ = ['_p', '_sze', 'arr']
    def __init__(self, **kwargs):
        self._p = Vec2(0, 0)
        self._cropop = Crop((0, 0), self._sze)
        NormalisedOp.__init__(self, **kwargs)
    @property
    def pos(self):
        return self._p
    @pos.setter
    def pos(self, *args):
        self._p = Vec2(*args)
    def apply(self, mat: np.ndarray, arr: np.ndarray, crop, defSmth):
        self._cropop.rect = (*self._p, *self._sze)
        args = self._cropop.apply(mat, crop, defSmth)
        if args is not None:
            mat, crop, defSmth = args
            _basey.blit(mat @ self._p.mat, self.arr, arr, crop)
        return arr

    def rect(self):
        return (*self._p, *self._sze)
    def _translate(self, *args):
        self._p += args

class Surf(_SurfaceBase, _SurfaceBase2):
    @overload
    def __init__(self, wid: float, height: float, *, normalise_x = None, normalise_y = None): ...
    @overload
    def __init__(self, sze, *, normalise_x = None, normalise_y = None): ...
    def __init__(self, *args, **kwargs):
        match len(args):
            case 1:
                _SurfaceBase.__init__(self, args[0])
            case 2:
                _SurfaceBase.__init__(self, args)
            case _:
                raise TypeError(
                    f'Incorrect number of arguments! Expected 1 or 2, found {len(args)}!'
                )
        _SurfaceBase2.__init__(self, **kwargs)

class Image(_SurfaceBase2):
    __slots__ = ['_im', '_arr']
    def __init__(self, pth: str, *, normalise_x = None, normalise_y = None):
        self._arr = None
        self.image = _PillowImg.open(pth)
        super().__init__(normalise_x=normalise_x, normalise_y=normalise_y)

    @property
    def _sze(self):
        return self._im.size
    @property
    def arr(self):
        if self._arr is None:
            self._arr = np.asarray(self._im)
        return self._arr
    @property
    def image(self):
        return self._im
    @image.setter
    def image(self, new):
        self._arr = None
        if new.mode != 'RGBA':
            self._im = new.convert('RGBA')
        else:
            self._im = new

def Preserve(op: NormalisedOp) -> Surf:
    if not hasattr(op, 'rect'):
        raise ValueError(
            'Op is not normalised - it has no rect function!'
        )
    x, y, wid, hei = op.rect()
    if x is None:
        raise ValueError(
            'Op seems normalised but rect returns None!'
        )
    s = Surf(wid, hei)(op)
    s._p = x, y
    return s

