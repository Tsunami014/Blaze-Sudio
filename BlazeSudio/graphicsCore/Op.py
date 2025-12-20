from .base import Op, MatOp, OpFlags
from typing import overload, Iterable
import numpy as np
import math

__all__ = [
    'Transform',
    'Translate',
    'Rotate',
    'Scale',
    'Resize',
    #'Crop',
    'Fill'
]

class Transform(MatOp):
    def __init__(
        self, *,
        rotation = 0,
        translate = (0, 0),
        scale = (1, 1),
        centre = True,
        smooth: bool = None
    ):
        if rotation == 0:
            cos = 1
            sin = 0
        else:
            cos = math.cos(rotation)
            sin = math.sin(rotation)

        super().__init__([
            [scale[0]*cos, -sin,         translate[0]],
            [sin,          scale[1]*cos, translate[1]],
            [0,            0,            1]
        ], centre, smooth)

class Translate(MatOp):
    @overload
    def __init__(self, pos: Iterable[int], /,*, smooth: bool = None): ...
    @overload
    def __init__(self, x: int, y: int, /,*, smooth: bool = None): ...
    def __init__(self, *args, smooth: bool = None):
        match len(args):
            case 1:
                x, y = args[0]
            case 2:
                x, y = args
            case _:
                raise TypeError(
                    f'Expected 1 or 2 arguments, found {len(args)}!'
                )
        super().__init__([
            [1, 0, x],
            [0, 1, y],
            [0, 0, 1]
        ], False, smooth)

class Rotate(MatOp):
    def __init__(self, angle, /,*, centre: bool = True, smooth: bool = None):
        if angle == 0:
            cos = 1
            sin = 0
        else:
            rads = math.radians(angle)
            cos = math.cos(rads)
            sin = math.sin(rads)
        super().__init__([
            [cos, -sin, 0],
            [sin, cos,  0],
            [0,   0,    1]
        ], centre, smooth)

class Scale(MatOp):
    @overload
    def __init__(self, sze: Iterable[int], /,*, centre: bool = True, smooth: bool = None): ...
    @overload
    def __init__(self, wid: int, hei: int, /,*, centre: bool = True, smooth: bool = None): ...
    def __init__(self, *args, centre = True, smooth = None):
        match len(args):
            case 2:
                sze = (args[0], args[1])
            case 1:
                sze = args[0]
                if len(sze) != 2:
                    raise TypeError(
                        f'Size must be an iterable with length 2, found length {len(sze)}!'
                    )
            case _:
                raise TypeError(
                    f'Expected 1 or 2 arguments, found {len(args)}!'
                )
        super().__init__([
            [sze[0], 0,      0],
            [0,      sze[1], 0],
            [0,      0,      1]
        ], centre, smooth)

class Resize(MatOp):
    __slots__ = ['sze', 'centre2']

    @overload
    def __init__(self, sze: Iterable[int], /,*, centre: bool = True, smooth: bool = None): ...
    @overload
    def __init__(self, wid: int, hei: int, /,*, centre: bool = True, smooth: bool = None): ...
    def __init__(self, *args, centre = True, smooth = None):
        match len(args):
            case 2:
                sze = (args[0], args[1])
            case 1:
                sze = args[0]
                if len(sze) != 2:
                    raise TypeError(
                        f'Size must be an iterable with length 2, found length {len(sze)}!'
                    )
            case _:
                raise TypeError(
                    f'Expected 1 or 2 arguments, found {len(args)}!'
                )

        super().__init__([
            [sze[0], 0,      0],
            [0,      sze[1], 0],
            [0,      0,      0]
        ], True, smooth)
        self.centre2 = centre

    def centredMat(self, arr: np.ndarray) -> np.ndarray:
        h, w, _ = arr.shape
        mat = np.array(self.mat / [w, h, 1], float)
        if not self.centre2:
            return mat
        hw, hh = w/2, h/2
        T1 = np.array([[1, 0, -hw],[0, 1, -hh],[0, 0, 1]], float)
        T2 = np.array([[1, 0, hw], [0, 1, hh], [0, 0, 1]], float)
        return T1 @ mat @ T2

#class Crop


class Fill(Op):
    __slots__ = ['col']
    def __init__(self, col):
        self.col = np.array(col, np.uint8)
        self.flags = OpFlags.NoFlags
    def apply(self, arr: np.ndarray, _):
        if (self.col[0] == self.col[1] == self.col[2]).all():
            arr.fill(self.col[0])
        else:
            arr[...] = self.col
        return arr

