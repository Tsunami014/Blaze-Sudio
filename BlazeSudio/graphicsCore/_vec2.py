from typing import overload

class Vec2:
    __slots__ = ['pos']

    @overload
    def __init__(self, x: float, y: float): ...
    @overload
    def __init__(self, pos): ...
    def __init__(self, *args):
        match len(args):
            case 1:
                self.pos = args[0]
            case 2:
                self.pos = args
            case _:
                raise TypeError(
                    f'Expected 1 or 2 arguments, found {len(args)}!'
                )

    @property
    def x(self) -> float:
        return self.pos[0]
    @property
    def y(self) -> float:
        return self.pos[1]

    def __iter__(self):
        return iter(self.pos)
    def __len__(self):
        return 2
    def __getitem__(self, it):
        return self.pos[it]

    def __neg__(self):
        return Vec2(-self.pos[0], -self.pos[1])
    def __abs__(self):
        return Vec2(abs(self.pos[0]), abs(self.pos[1]))

    def __add__(self, oth):
        return Vec2(self.pos[0] + oth[0], self.pos[1] + oth[1])
    def __sub__(self, oth):
        return Vec2(self.pos[0] - oth[0], self.pos[1] - oth[1])
    def __mul__(self, oth):
        return Vec2(self.pos[0] * oth[0], self.pos[1] * oth[1])
    def __floordiv__(self, oth):
        return Vec2(self.pos[0] // oth[0], self.pos[1] // oth[1])
    def __div__(self, oth):
        return Vec2(self.pos[0] / oth[0], self.pos[1] / oth[1])

