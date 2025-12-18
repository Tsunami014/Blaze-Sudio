from .base import Op, MatOp, OpFlags
from typing import overload, Iterable
import numpy as np

__all__ = [
    'Scale',
    'Resize',
    'Fill'
]

class Transform(MatOp):
    def __init__(
        self, *,
        translate=(0, 0),
        scale=(1, 1),
        smooth: bool = None
    ):
        super().__init__([
            [scale[0], 0,        translate[0]],
            [0,        scale[1], translate[1]],
            [0,        0,        1]
        ], smooth)

class Scale(MatOp):
    @overload
    def __init__(self, sze: Iterable[int], /, smooth: bool = None): ...
    @overload
    def __init__(self, wid: int, hei: int, /, smooth: bool = None): ...
    def __init__(self, *args, smooth: bool = None):
        if args[-1] is True or args[-1] is False:
            if smooth is not None:
                raise ValueError(
                    'Last argument is a bool for smooth, but smooth is also defined as a keyword!'
                )
            smooth = args[-1]
            args = args[:-1]
        if len(args) == 1:
            sze = args[0]
            if len(sze) != 2:
                raise TypeError(
                    f'Size must be an iterable with length 2, found length {len(sze)}!'
                )
        elif len(args) == 2:
            sze = (args[0], args[1])
        else:
            raise TypeError(
                f'Expected 1-2 arguments, found {len(args)}!'
            )
        super().__init__([
            [sze[0], 0,      0],
            [0,      sze[1], 0],
            [0,      0,      1]
        ], smooth)

class Resize(Op): # FIXME
    __slots__ = ['sze', '_smooth']

    @overload
    def __init__(self, sze: Iterable[int], /, smooth: bool = None): ...
    @overload
    def __init__(self, wid: int, hei: int, /, smooth: bool = None): ...
    def __init__(self, *args, smooth: bool = None):
        if args[-1] is True or args[-1] is False:
            if smooth is not None:
                raise ValueError(
                    'Last argument is a bool for smooth, but smooth is also defined as a keyword!'
                )
            smooth = args[-1]
            args = args[:-1]
        if len(args) == 1:
            sze = args[0]
            if len(sze) != 2:
                raise TypeError(
                    f'Size must be an iterable with length 2, found length {len(sze)}!'
                )
        elif len(args) == 2:
            sze = (args[0], args[1])
        else:
            raise TypeError(
                f'Expected 1-2 arguments, found {len(args)}!'
            )

        self.sze = sze
        self._smooth = smooth
        self.flags = OpFlags.NoFlags

    def apply(self, arr: np.ndarray, defSmth: bool):
        smooth = self._smooth if self._smooth is not None else defSmth
        return arr # TODO: This


class Fill(Op):
    __slots__ = ['col']
    def __init__(self, col):
        self.col = col
        self.flags = OpFlags.NoFlags
    def apply(self, arr: np.ndarray, _):
        arr[:] = self.col
        return arr

