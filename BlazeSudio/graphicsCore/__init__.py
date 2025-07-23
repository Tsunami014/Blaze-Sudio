from BlazeSudio.graphicsCore import base
from BlazeSudio.graphicsCore.apply import Apply
from typing import overload, Iterable, Tuple
from collections import deque
import time
import pygame
pygame.init()

__all__ = [
    'Quit',
    'Interaction',
    'Window',
    'Surface',
    'Clock'
]


def Quit():
    """
    Quits the application, handling all quit code accordingly
    """
    pygame.quit()

class Clock():
    def __init__(self):
        self.dt = 0
        self._lastTime = None

    def tick(self, maxfps: int|float = None):
        """
        Ticks the clock, updating FPS count and optionally enforcing a maximum FPS.

        Args:
            maxfps: The maximum fps the application should run at. Defaults to None (don't enforce)
        """
        t = time.time()
        slept = False
        if self._lastTime is not None:
            # raw delta-time
            delta = t - self._lastTime
            # enforce max FPS if requested
            if maxfps is not None:
                target_dt = 1.0 / maxfps
                if delta < target_dt:
                    slept = True
                    time.sleep(target_dt - delta - 0.001)
                    t = time.time()
                    delta = t - self._lastTime
            self.dt = delta
        if not slept:
            time.sleep(0)
        self._lastTime = t

    def get_fps(self):
        """
        Returns the number of frames per second instantly
        """
        return 0 if self.dt == 0 else 1.0 / self.dt

class AvgClock(Clock):
    def __init__(self, secs: int|float):
        """
        An average Clock, averaging the fps over a set time.

        Args:
            secs: The number of seconds to average the fps over
        """
        self.secs = secs
        self._frameTimes = deque()
        super().__init__()

    def tick(self, maxfps: int|float = None):
        """
        Ticks the clock, updating FPS count and optionally enforcing a maximum FPS.

        Args:
            maxfps: The maximum fps the application should run at. Defaults to None (don't enforce)
        """
        super().tick(maxfps)
        # record this tick
        self._frameTimes.append(self._lastTime)
        # drop any frames older than time s
        cutoff = self._lastTime - self.secs
        while self._frameTimes and self._frameTimes[0] < cutoff:
            self._frameTimes.popleft()

    def get_fps(self):
        """
        Returns the average FPS over the last secs seconds.
        """
        count = len(self._frameTimes)
        return count / self.secs if self.secs > 0 else 0

    def get_fps_inst(self):
        """
        Returns the number of frames per second instantly
        """
        return super().get_fps()

class Colour: # TODO: themes - repeated colours (and 'highlight 1', 'tone 3', etc.) put in a list so apps can easily theme switch
    """
    A Colour is a hex value represented as an integer.
    
    This class gives some helper functions for creating these tuples based off of different colour types.

    FYI: `Colour(r, g, b)` is a shorter way of writing `Colour.from_rgb(r, g, b)`
    """
    _RGBHEXFMT = "{0:02x}{1:02x}{2:02x}"
    def __new__(cls, *args):
        """
        A shorter form of `Colour.from_rgb(r, g, b)`
        """
        return cls.from_rgb(*args)
    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> int:
        def clamp(x): 
            assert 0 <= x <= 255, "RGB value must be between 0-255!"
            return x
        return int(cls._RGBHEXFMT.format(clamp(r), clamp(g), clamp(b)), 16)
    @classmethod
    def from_hex(cls, hex: str) -> int:
        return int(hex.lstrip("#"), 16)
    @classmethod
    def to_rgb(cls, col: int) -> Iterable[int]:
        return [(col >> 8*i) & 0xFF for i in (2, 1, 0)]
    @classmethod
    def to_hex(cls, col: int, upper=True) -> str:
        if upper:
            return "#"+hex(col)[2:].upper()
        return "#"+hex(col)[2:]
    # TODO: to/from hsv

class Interaction:
    class Keys(type):
        """
        A wrapper for the pygame keys.

        Gets the keycode for a specific key.

        You can use 2 methods for getting keys:
        1. `Keys.a` for the 'a' key
        2. `Keys.K_a` for the 'a' key (useful for e.g. numbers `Keys.K_0`)
        """
        def __getattribute__(cls, name):
            if name.startswith('K_'):
                return pygame.key.key_code(name[2:])
            return pygame.key.key_code(name)
    
    @staticmethod
    def eventGet(eventtype: Iterable|None = None) -> Iterable[pygame.event.Event]:
        """
        Get the events that have occurred

        Args:
            eventtype (Iterable[EventTypes] | None, optional): The event types to get specifically. Defaults to all of them.

        Returns:
            Iterable[pygame.event.Event]: A list of pygame.event.Event's.
        """
        return pygame.event.get(eventtype)
    @staticmethod
    def eventHandleBasic() -> bool:
        """
        Handles all events, returning True if need to quit (escape key or pygame.QUIT recieved)

        Returns:
            bool: Whether the application should quit (True) or continue running (False)
        """
        return not any(
            i.type == pygame.QUIT or \
            (i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE)
                for i in pygame.event.get()
        )
    @staticmethod
    def eventPump() -> None:
        """
        Pump the events so the OS doesn't kill the app due to inactivity
        """
        pygame.event.pump()
    
    @staticmethod
    def keyPress() -> pygame.key.ScancodeWrapper:
        """
        Gets a list of all the keys currently pressed.

        Indexable through `keys[Keys.K_0]` for the 0 key, etc.
        """
        return pygame.key.get_pressed()
    @staticmethod
    def keyMods() -> pygame.key.ScancodeWrapper:
        """
        Gets a list of all the modifier keys currently pressed.

        Indexable through `mods & Keys.` for the 0 key, etc.
        """
        return pygame.key.get_mods()
    
    @staticmethod
    def mousePos() -> Tuple[int, int]:
        """
        Get the mouse position

        Returns:
            Tuple[int, int]: The mouse position; x, y
        """
        return pygame.mouse.get_pos()
    @staticmethod
    def mousePress() -> Tuple[bool, bool, bool]:
        """
        Get the mouse buttons that are pressed

        Returns:
            Tuple[bool, bool, bool]: Which buttons are pressed: [left, middle, right]
        """
        return pygame.mouse.get_pressed()

class Window:
    _PGWIN: pygame.Surface = None
    _WINDOW: 'Surface' = None
    def __new__(cls, *args, **kwargs):
        return cls._WINDOW
    
    @classmethod
    def flush(cls):
        """
        Print the current window to the screen
        """
        cls._PGWIN.blit(cls._WINDOW.to_pygame(), (0, 0))

    @overload
    @classmethod
    def create_win(**kwargs) -> 'Surface':
        """
        Creates the window fullscreen, with optional kwargs for creation

        Args:
            **kwargs: Kwargs passed to pygame.display.set_mode
        
        Returns:
            Surface: The created surface
        """
    @overload
    @classmethod
    def create_win(cls, sze: Iterable[int], **kwargs) -> 'Surface':
        """
        Create the window with a set size, with optional kwargs for creation

        Args:
            sze (Iterable[int]): The size of the new window
        
            **kwargs: Kwargs passed to pygame.display.set_mode
        
        Returns:
            Surface: The created surface
        """
    @overload
    @classmethod
    def create_win(cls, width: int, height: int, **kwargs) -> 'Surface':
        """
        Create the window with a set size, with optional kwargs for creation

        Args:
            width (int): The width of the new window
            height (int): The height of the new window
        
            **kwargs: Kwargs passed to pygame.display.set_mode
        
        Returns:
            Surface: The created surface
        """
    @classmethod
    def create_win(cls, *args, **kwargs):
        if len(args) == 0:
            sze = (0, 0)
        elif len(args) == 1:
            if len(args[0]) != 2:
                raise TypeError(
                    f'Expected size argument to have length 2, found {len(args[0])}!'
                )
            sze = (args[0][0], args[0][1])
        elif len(args) == 2:
            sze = (args[0], args[1])
        else:
            raise TypeError(
                f'Too many positional arguments! Expected 0-2, found {len(args)}!'
            )
        cls._PGWIN = pygame.display.set_mode(sze, **kwargs)
        if sze[0] == 0 and sze[1] == 0:
            if not pygame.display.is_fullscreen():
                pygame.display.toggle_fullscreen()
            sze = cls._PGWIN.get_size()
        elif pygame.display.is_fullscreen():
            pygame.display.toggle_fullscreen()
        
        cls._WINDOW = Surface(sze)
        cls._WINDOW._WinSur = True
        return cls._WINDOW

    @classmethod
    def update(cls, rect=None):
        """
        Update the screen; only the portion that changed

        Args:
            rect (Rect | Iterable[Rect] | None): The rectangle to update
        """
        pygame.display.update(rect)
    
    @classmethod
    def flip(cls):
        """
        Update the entire screen. Marginally faster than .update when updating the entire screen
        """
        pygame.display.flip()
    
    @classmethod
    def set_title(cls, title: str, icontitle: str|None = None):
        """
        Set the title of the window

        Args:
            title (str): The new title of the window
            icontitle (str | None, optional): Assumedly, the title of the icon. Defaults to None. TODO: Check pygame docs about this
        """
        pygame.display.set_caption(title, (title if icontitle is None else icontitle))
    @classmethod
    def set_icon(cls, icon: 'Surface'):
        pygame.display.set_icon(icon())
    
    @classmethod
    def fill(cls, col: Iterable[int]):
        """
        _summary_

        Args:
            col (Iterable[int]): _description_
        """
        cls._PGWIN.fill(col)

# TODO: Cache - use cached surface OR
# modify the cached surface (keeping existing operations) if there aren't that many and only additions and not resizing, rotating, etc. OR
# completely redo it again
class Surface(base.AllFuncs, Apply):
    __slots__ = ['_ops', '_WinSur']
    @overload
    def __init__(self, width: int, height: int):
        """
        Create a Surface class

        Args:
            width (int): The width of the new surface
            height (int): The height of the new surface
        """
    @overload
    def __init__(self, size: Iterable[int]):
        """
        Create a Surface class

        Args:
            size (Iterable[int]): The size of the new surface
        """
    def __init__(self, *args):
        """
        Creates a surface
        """
        self._WinSur = False
        if len(args) == 1:
            self._ops = [base.SizeOp(args[0])]
        elif len(args) == 2:
            self._ops = [base.SizeOp((args[0], args[1]))]
        else:
            raise TypeError(
                f'Expected 1-2 args, found {len(args)}!'
            )
    
    def Test(self):
        """
        Generate this surface, then apply to the pygame window and display it. Used in testing.

        This is for if you want to see what a surface looks like when debugging.
        """
        if not self._WinSur:
            Window.fill((0, 0, 0))
            Window() # TODO: .blit
        Window.flush()
        Window.flip()
    
    def copy(self):
        pass
