import numpy as np
from .base import MatOp, Op
from _typeshed import Incomplete
from typing import Iterable, overload

__all__ = ['Scale', 'Resize', 'Fill']

class Transform(MatOp):
    def __init__(self, *, translate=(0, 0), scale=(1, 1), smooth: bool = None) -> None: ...

class Scale(MatOp):
    @overload
    def __init__(self, sze: Iterable[int], /, smooth: bool = None) -> None: ...
    @overload
    def __init__(self, wid: int, hei: int, /, smooth: bool = None) -> None: ...

class Resize(Op):
    @overload
    def __init__(self, sze: Iterable[int], /, smooth: bool = None) -> None: ...
    @overload
    def __init__(self, wid: int, hei: int, /, smooth: bool = None) -> None: ...
    def apply(self, arr: np.ndarray, defSmth: bool): ...

class Fill(Op):
    col: Incomplete
    flags: Incomplete
    def __init__(self, col) -> None: ...
    def apply(self, arr: np.ndarray, _): ...
