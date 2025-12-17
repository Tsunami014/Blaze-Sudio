from .Events import EvTyp as EvTyp, Event as Event
from typing import Iterable

__all__ = ['EvTyp', 'Event', 'Keys', 'update']

class Keys:
    '''
    Get keys pressed or key events

    - Is a key pressed? Use e.g. `Keys["a"]` (note this does not differentiate against \'A\' and \'a\')
    - Has a key event happened? Use the `Keys.event` function
    - Are any keyboard modifiers pressed? Use the booleans starting with `m` - e.g. `Keys.mShift`, `Keys.mCtrl` or `Keys.mAlt`
    '''
    mShift: bool
    mCtrl: bool
    mAlt: bool
    mGui: bool
    mNumLock: bool
    mCapsLock: bool
    def __getitem__(cls, key): ...
    def events() -> None: ...

class Mouse:
    """
    Get mouse buttons/movement

    - Is a mouse button pressed? Use e.g. `Mouse.left`
    - Mouse position? Use `Mouse.pos`, `Mouse.x` or `Mouse.y`
    - Set the mouse position? Use e.g. `Mouse.x = 10` (can set x, y or pos)
    """
    left: bool
    l: bool
    middle: bool
    m: bool
    right: bool
    r: bool
    x1: bool
    x2: bool
    pos: Iterable[int]
    x: int
    y: int
    def __getattr__(self, name): ...
    def __setattr__(self, name, value): ...

def update() -> None:
    """
    Updates interaction stuff!
    """
