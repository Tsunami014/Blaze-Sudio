from .base import NormalisedOp, Vec2
from . import _basey
import numpy as np
from PIL import Image as _PillowImg

class Surface(NormalisedOp):
    __slots__ = ['_im', '_arr', 'offs']
    def __init__(self, im: _PillowImg, *, normalise_x = None, normalise_y = None):
        self._arr = None
        self.image = im
        self.offs = Vec2(0, 0)
        super().__init__(normalise_x=normalise_x, normalise_y=normalise_y)
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
    def apply(self, mat: np.ndarray, arr: np.ndarray, crop, defSmth):
        _basey.blit(mat @ self.offs.mat, self.arr, arr, crop)
        return arr

    def rect(self):
        """Returns a tuple in the format (topleft_x, topleft_y, width, height)"""
        return (*self.offs, *self._im.size)
    def _translate(self, *args):
        self.offs += args

class Image(Surface):
    __slots__ = []
    def __init__(self, pth: str, *, normalise_x = None, normalise_y = None):
        super().__init__(_PillowImg.open(pth), normalise_x=normalise_x, normalise_y=normalise_y)

