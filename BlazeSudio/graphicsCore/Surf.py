from .base import NormalisedOp, Vec2
from . import _basey
import numpy as np
from PIL import Image as _PillowImg

class Surface(NormalisedOp):
    __slots__ = ['im', 'offs']
    def __init__(self, im: _PillowImg, *, normalise_x = None, normalise_y = None):
        if im.mode != 'RGBA':
            self.im = im.convert('RGBA')
        else:
            self.im = im
        self.offs = Vec2(0, 0)
        super().__init__(normalise_x=normalise_x, normalise_y=normalise_y)
    def apply(self, mat: np.ndarray, arr: np.ndarray, crop, defSmth):
        _basey.blit(mat @ self.offs.mat, np.asarray(self.im), arr, crop)
        return arr

    def rect(self):
        """Returns a tuple in the format (topleft_x, topleft_y, width, height)"""
        return self.im.size
    def _translate(self, *args):
        self.offs += args

class Image(Surface):
    __slots__ = []
    def __init__(self, pth: str, *, normalise_x = None, normalise_y = None):
        super().__init__(_PillowImg.open(pth), normalise_x=normalise_x, normalise_y=normalise_y)

