import numpy as np
from abc import ABC, abstractmethod
from enum import IntEnum

__all__ = [
    'OpsList',
    'Op',
        'ElmOp',
    'Func'
]

class OpsList(IntEnum):
    Size = 1
    Fill = 2
    Poly = 3

class Op(ABC):
    __slots__ = []
    typ: OpsList = None
    isElm: bool = False
    @abstractmethod
    def __init__():
        pass
class ElmOp(Op):
    isElm: bool = True
    @abstractmethod
    def ApplyOp(self, op: 'Op') -> bool: # Returns whether to keep the element or not
        return True
    @abstractmethod
    def ApplyOnArr(self, arr: np.ndarray):
        pass
class Func(ABC):
    __slots__ = ['_ops']
    _ops: list[Op]
    def __init__():
        pass
