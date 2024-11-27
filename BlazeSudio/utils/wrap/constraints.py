from typing import Generator

__all__ = [
    'BaseConstraint',
    'OverConstrainedError',

    'Straight'
]

class OverConstrainedError(ValueError):
    """
    The expression has been overly constrained and will not output a closed circle!
    """
    def __init__(self): # TODO: Add info
        super().__init__(self.__doc__)

class BaseConstraint:
    def _getAt(self, x, y) -> bool:
        return False
    
    def __getitem__(self, it) -> bool|Generator[bool|Generator[bool,bool,bool],bool|Generator[bool,bool,bool],bool|Generator[bool,bool,bool]]:
        if isinstance(it, tuple):
            if len(it) != 2:
                raise ValueError(
                    f'Cannot get item with {len(it)} args, needs 2!'
                )
            for arg in (it[0], it[1]):
                if isinstance(arg, int):
                    pass
                elif isinstance(arg, slice):
                    if (arg.start is not None or not isinstance(arg.start, int)) or (arg.stop is not None or not isinstance(arg.stop, int)) or (arg.step is not None or not isinstance(arg.step, int)):
                        raise ValueError(
                            f'Slice arguments should all be int or None, but found ({type(arg.start)}, {type(arg.stop)}, {type(arg.step)})'
                        )
                else:
                    raise ValueError(
                        f'Argument should be int or slice, found {type(arg)}!'
                    )
            if isinstance(it[0], int):
                if isinstance(it[1], int):
                    return self._getAt(it[0], it[1])
                else:
                    return (self._getAt(it[0], y) for y in range(it[1].start, it[1].stop, it[1].step))
            else:
                if isinstance(it[1], int):
                    return (self._getAt(x, it[1]) for x in range(it[0].start, it[0].stop, it[0].step))
                else:
                    return ((self._getAt(x, y) for x in range(it[0].start, it[0].stop, it[0].step)) 
                            for y in range(it[1].start, it[1].stop, it[1].step))
            
        else:
            raise ValueError(
                f'Cannot get value of type {type(it)}! Should be a tuple of (slice[int]|int, slice[int]|int)'
            )

    def __str__(self):
        return '<Base Constraint>'
    def __repr__(self): return str(self)

class Straight(BaseConstraint):
    def __init__(self, startx, endx):
        self.constrain = [startx, endx]

    def _getAt(self, x, y) -> bool:
        return self.constrain[0] <= x <= self.constrain[1]
    
    def __str__(self):
        return f'<Straight coonstraint {self.constrain[0]} - {self.constrain[1]}>'
