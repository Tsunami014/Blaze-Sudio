from .base import OpFlags, Anchors, Vec2
from . import Trans, Draw, Surf, base
from typing import overload
import numpy as np

__all__ = [
    'Trans', 'Draw', 'Surf',
    'Anchors',
    'Vec2',

    'Fill',
    'Crop'
]

class Fill(base.Op):
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

class Crop(base.Trans, base._basey.TransBase):
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

