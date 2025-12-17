import numpy as np
from . import base as b
from typing import Iterable, overload

__all__ = ['Surface']

class Surface:
    @overload
    def __init__(self, width: int, height: int, /) -> None:
        """
        Create a Surface with a set width and height

        Args:
            width (int): The width of the new surface
            height (int): The height of the new surface
        """
    @overload
    def __init__(self, size: Iterable[int]) -> None:
        """
        Create a Surface with a set size

        Args:
            size (Iterable[int]): The size of the new surface
        """
    @overload
    def __init__(self, arr: np.ndarray) -> None:
        """
        Create a Surface from an array
        """
    isSmooth: bool
    def rough(self) -> Surface: ...
    def smooth(self) -> Surface: ...
    @property
    def size(self) -> Iterable[int]: ...
    def toNumpy(self, op: b.Op) -> np.ndarray:
        """
        Get the numpy array image of this surface!
        """
    @overload
    def blit(self, pos: Iterable[int], sze: Iterable[int] = None, /) -> b.Op:
        """
        Get the operation for blitting this at `pos` and optionally cropped to `sze`.
        """
    @overload
    def blit(self, x: int, y: int, wid: int = None, hei: int = None, /) -> b.Op:
        """
        Get the operation for blitting this at `(x, y)` and optionally cropped to `(wid, hei)`.
        """
    def __matmul__(self, other: b.Op): ...
    def __setitem__(self, idx) -> None: ...
    def copy(self) -> None: ...

class Window(Surface):
    @overload
    def __init__(self) -> None:
        """
        Create a fullscreen window
        """
    @overload
    def __init__(self, sze: Iterable[int]) -> None:
        """
        Create a window. If resized to (0, 0), will become fullscreen.

        Args:
            sze (Iterable[int]): The size of the new window
        """
    @overload
    def __init__(self, width: int, height: int, /) -> None:
        """
        Create a window. If resized to (0, 0), will become fullscreen.

        Args:
            width (int): The width of the new window
            height (int): The height of the new window
        """
    def Quit(self) -> None:
        """
        Quits the application, handling all quit code accordingly
        """
    @property
    def size(self) -> Iterable[int]: ...
    def rough(self) -> Window: ...
    def smooth(self) -> Window: ...
    @overload
    def resize(self) -> None:
        """
        Resize the window to fullscreen
        """
    @overload
    def resize(self, sze: Iterable[int]):
        """
        Resize the window. If resized to (0, 0), will become fullscreen.

        Args:
            sze (Iterable[int]): The size of the new window
        """
    @overload
    def resize(self, width: int, height: int, /):
        """
        Resize the window. If resized to (0, 0), will become fullscreen.

        Args:
            width (int): The width of the new window
            height (int): The height of the new window
        """
    def __matmul__(self, other: b.Op): ...
    def clear(self) -> None: ...
    def cleared(self) -> Window: ...
    def rend(self) -> None:
        """
        Render the entire screen.
        """
    def set_title(self, title: str):
        """
        Set the title of the window

        Args:
            title (str): The new title of the window
        """
    def set_icon(self, icon: Surface): ...
