from .base import Op, OpFlags, Anchors
from . import Trans, Draw
import numpy as np

__all__ = [
    'Trans', 'Draw',
    'Anchors',

    'Fill'
]

class Fill(Op):
    __slots__ = ['col']
    def __init__(self, col):
        self.col = np.array(col, np.uint8)
        self.flags = OpFlags.Reset
    def apply(self, _, arr: np.ndarray, __):
        if (self.col[0] == self.col[1] == self.col[2]).all():
            arr.fill(self.col[0])
        else:
            arr[...] = self.col
        return arr

#class Crop

