import numpy as np
from typing import overload, Iterable
from BlazeSudio.graphicsCore.basebase import Op, ElmOp, Func, OpsList
from BlazeSudio.graphicsCore.draw import _DrawFuncs

class SizeOp(Op):
    __slots__ = ['sze']
    typ = OpsList.Size
    @overload
    def __init__(self, sze): ...
    @overload
    def __init__(self, wid, hei): ...
    def __init__(self, *args):
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
        
        self.sze = np.array(sze, dtype=np.uint64)
class SizeFunc(Func):
    @overload
    def resize(self, size: Iterable[int]):
        """
        Resize the surface to a new size

        Args:
            size (Iterable[int]): The new size
        """
    @overload
    def resize(self, width: int, height: int):
        """
        Resize the surface to a new size

        Args:
            width (int): The new width
            height (int): The new height
        """
    def resize(self, *args):
        if len(self._ops) != 0 and self._ops[-1].typ == OpsList.Size:
            nsze = SizeOp(*args)
            self._ops[-1].sze += nsze.sze
        else:
            self._ops.append(SizeOp(*args))

class FillOp(ElmOp):
    __slots__ = ['col']
    typ = OpsList.Fill
    def __init__(self, col):
        self.col = col
    
    def ApplyOp(self, op):
        return True
    def ApplyOnArr(self, arr: np.ndarray):
        arr.fill(self.col)
class FillFunc(Func):
    # TODO: Overloads for fill
    def fill(self, col: Iterable[int]):
        """
        Fills a surface with a colour, removing all previous operations except for resizes (as the fill overlays over entire screen anyway)

        Args:
            col (Iterable[int]): The colour to fill the surface with
        """
        for op in reversed(self._ops):
            if op.typ == OpsList.Size:
                self._ops = [SizeOp(op.sze), FillOp(col)]
                return
        self._ops = [FillOp(col)]

class AllFuncs(SizeFunc, FillFunc, _DrawFuncs):
    pass
