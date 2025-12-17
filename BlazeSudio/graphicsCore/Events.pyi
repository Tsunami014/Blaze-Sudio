from _typeshed import Incomplete
from enum import IntEnum
from typing import Self, TypeVar

__all__ = ['EvTyp', 'Event', 'EVENT_LIST', '_translateEv']

class EvTyp(IntEnum):
    Quit = 0
    Keyboard = 1
    KeyDown = 17
    KeyUp = 33
    KeyType = 49
    KeyTyping = 65
    Mouse = 2
    MouseClick = 18
    MouseDown = 274
    MouseUp = 530
    MouseMove = 34
    MouseScroll = 50
    FileDrop = 3
    FileDropStart = 19
    FileDropEnd = 35
    FileDropText = 51
    FileDropFile = 67
    Controller = 4
    ContrDevice = 20
    ContrDevConnect = 276
    ContrDevDiscon = 532
    ContrDevRemap = 788
    ContrAxis = 36
    ContrBtn = 52
    ContrBtnDown = 308
    ContrBtnUp = 564
    ContrSensor = 68
    Touch = 5
    TouchSingle = 21
    TouchMulti = 37
    TouchDollar = 53
    Clipboard = 6
    Audio = 7
    AudioAdded = 23
    AudioRemoved = 39
    Sensor = 8
    Window = 9
    User = 15
T = TypeVar('T')

class Event:
    timestamp: int
    typ: int
    def __new__(cls, var: Event, typ: int = None) -> Self:
        """
        Check and type convert to an Event type

        This checks if the input `var` is of a type and returns the var if it is or False if it is not.

        If `typ` is set it checks if the type of the object is like the type specified,
        and if unset it checks against all the types this class can contain.
        `typ` must be a type that can be found in this class.

        A type that is 'like' this is e.g. if this class handled `ContrDevConnect` events, you could specify type `ContrDevice`.

        Example usage: for checking if the event `event` is an escape key with type hinting:
        ```py
        if (keyev := KeyEvent(event, EvTyp.KeyDown)) and keyev.key == 'Escape':
            ... # Can use keyev here for type hinting
        ```
        """
    def __init__(self, *args, **kwargs) -> None: ...
    @classmethod
    def create(cls, **kwargs):
        """
        Create a new event object. Not for the light-hearted.
        """

class QuitEvent(Event): ...

class KeyEvent(Event):
    window_id: int
    state: bool
    repeat: bool
    @property
    def initial(self) -> bool:
        """True if this event is the first press of the key, False if it's repeating or releasing"""
    scancode: int
    keycode: int
    @property
    def scode(self) -> str:
        """The string name of the scancode"""
    @property
    def key(self) -> str:
        """The string name of the key"""
    def modifs(self, *, shift: bool = False, ctrl: bool = False, alt: bool = False, gui: bool = False) -> bool:
        """
        Find out if the specified modifiers are pressed when this key is

        Used like this: `ev.modifs(shift=1, ctrl=1)` returns if the shift and ctrl modifiers are pressed (can use True instead of 1 if desired)

        Modifiers present: `shift`, `ctrl`, `alt`, `gui` (windows/super/command key)
        """

EVENT_LIST: Incomplete

def _translateEv(ev): ...
