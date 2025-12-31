from . import base, _basey
from typing import overload, Iterable
import numpy as np
import ctypes
import sdl2
import copy

__all__ = ['Surface', 'Blit', 'Window']

class Blit(base.TransOp):
    __slots__ = ['arr', 'pos', 'sze']

    @overload
    def __init__(self, arr: np.ndarray, pos: Iterable[int] ,/) -> base.Op:
        """
        Paste a surface at `pos`
        """
    @overload
    def __init__(self, arr: np.ndarray, x: int, y: int ,/) -> base.Op:
        """
        Paste a surface at `(x, y)`
        """
    def __init__(self, *args):
        match len(args):
            case 2:
                self.arr, self.pos = args
            case 3:
                self.arr, x, y = args
                self.pos = (x, y)
        self.flags = base.OpFlags.Transformable

    def applyTrans(self, mat: np.ndarray, arr: np.ndarray) -> np.ndarray:
        if self.pos == (0, 0):
            _basey.blit(mat, self.arr, arr)
            return
        M = mat.copy()
        M[0, 2] += self.pos[0]
        M[1, 2] += self.pos[1]

        _basey.blit(M, self.arr, arr)
        return arr

# TODO: Make it not copy the array every @
class Surface:
    __slots__ = ['_arr', 'isSmooth']

    @overload
    def __init__(self, width: int, height: int ,/):
        """
        Create a Surface with a set width and height

        Args:
            width (int): The width of the new surface
            height (int): The height of the new surface
        """
    @overload
    def __init__(self, size: Iterable[int]):
        """
        Create a Surface with a set size

        Args:
            size (Iterable[int]): The size of the new surface
        """
    @overload
    def __init__(self, arr: np.ndarray):
        """
        Create a Surface from an array
        """
    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], np.ndarray):
                self._arr = args[0]
                self.isSmooth = False
                return
            size = args[0]
        elif len(args) == 2:
            size = (args[0], args[1])
        else:
            raise TypeError(
                f'Expected 1-2 args, found {len(args)}!'
            )
        self._arr = np.ndarray((size[1], size[0], 4), np.uint8)
        self.isSmooth = False

    def rough(self) -> 'Surface':
        self.isSmooth = False
        return self
    def smooth(self) -> 'Surface':
        self.isSmooth = True
        return self

    @property
    def size(self) -> Iterable[int]:
        return self._arr.shape[1], self._arr.shape[0]

    def toNumpy(self, op: base.Op) -> np.ndarray:
        """
        Get the numpy array image of this surface!
        """
        return op.apply(self._arr.copy(), self.isSmooth)

    @overload
    def blit(self, pos: Iterable[int], sze: Iterable[int] = None ,/) -> base.Op:
        """
        Get the operation for blitting this at `pos` and optionally cropped to `sze`.
        """
    @overload
    def blit(self, x: int, y: int, wid: int = None, hei: int = None ,/) -> base.Op:
        """
        Get the operation for blitting this at `(x, y)` and optionally cropped to `(wid, hei)`.
        """
    def blit(self, *args) -> Blit:
        return Blit(self._arr, *args)

    def __matmul__(self, other: base.Op):
        return Surface(self.toNumpy(other))

    def __getitem__(self, idx):
        if not isinstance(idx, tuple): # If only one value, it must be an x index or slice
            idx = (slice(None), idx)

        if len(idx) > 2:
            raise IndexError("Only 2D indexing [x, y] supported for Surface.")

        return self._arr[idx[1], idx[0]]

    def copy(self) -> 'Surface':
        new = Surface(self._arr.copy())
        new.isSmooth = self.isSmooth
        return new


_PIXFMT = sdl2.SDL_PIXELFORMAT_ABGR8888 # NOTE: This may display funny on big-endian systems (hopefully none that run this)
class Window(Surface):
    @overload
    def __init__(self):
        """
        Create a fullscreen window
        """
    @overload
    def __init__(self, sze: Iterable[int]):
        """
        Create a window. If resized to (0, 0), will become fullscreen.

        Args:
            sze (Iterable[int]): The size of the new window
        """
    @overload
    def __init__(self, width: int, height: int ,/):
        """
        Create a window. If resized to (0, 0), will become fullscreen.

        Args:
            width (int): The width of the new window
            height (int): The height of the new window
        """
    def __init__(self, *args):
        self._mainWin = sdl2.SDL_CreateWindow(b"Blaze Sudio game", 
                        sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, 0, 0, sdl2.SDL_WINDOW_SHOWN)
        flags = sdl2.SDL_RENDERER_ACCELERATED
        self._renderer = sdl2.SDL_CreateRenderer(self._mainWin, -1, flags)
        self._texture = sdl2.SDL_CreateTexture(self._renderer, _PIXFMT, sdl2.SDL_TEXTUREACCESS_STREAMING, 0, 0)

        self.resize(*args)
        self._op = None
        self.isSmooth = False
        self._cachedarr = None

    def Quit(self):
        """
        Quits the application, handling all quit code accordingly
        """
        sdl2.SDL_DestroyRenderer(self._renderer)
        sdl2.SDL_DestroyWindow(self._mainWin)
        sdl2.SDL_Quit()

    @property
    def size(self) -> Iterable[int]:
        return self._sze

    def rough(self) -> 'Window':
        self.smooth = False
        return self
    def smooth(self) -> 'Window':
        self.smooth = True
        return self
    
    @overload
    def resize(self):
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
    def resize(self, width: int, height: int ,/):
        """
        Resize the window. If resized to (0, 0), will become fullscreen.

        Args:
            width (int): The width of the new window
            height (int): The height of the new window
        """
    def resize(self, *args):
        if len(args) == 0:
            sze = (0, 0)
        elif len(args) == 1:
            if len(args[0]) != 2:
                raise TypeError(
                    f'Expected size argument to have length 2, found {len(args[0])}!'
                )
        elif len(args) == 2:
            sze = (args[0], args[1])
        else:
            raise TypeError(
                f'Too many positional arguments! Expected 0-2, found {len(args)}!'
            )

        self._cachedarr = None
        if sze[0] == 0 and sze[1] == 0:
            sdl2.SDL_SetWindowFullscreen(self._mainWin, sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP)
            w, h = ctypes.c_int(), ctypes.c_int()
            sdl2.SDL_GetWindowSize(self._mainWin, ctypes.byref(w), ctypes.byref(h))
            sze = (w.value, h.value)
        else:
            sdl2.SDL_SetWindowSize(self._mainWin, *sze)

        sdl2.SDL_DestroyTexture(self._texture)
        self._texture = sdl2.SDL_CreateTexture(self._renderer, _PIXFMT, sdl2.SDL_TEXTUREACCESS_STREAMING, *sze)
        self._sze = sze

    @property
    def _arr(self) -> np.ndarray:
        if self._cachedarr is None:
            arr = np.ndarray((self._sze[1], self._sze[0], 4), np.uint8)
            if self._op is not None:
                arr = self._op.apply(arr, self.isSmooth)
            self._cachedarr = arr
        return self._cachedarr

    def __matmul__(self, other: base.Op):
        self._op = other
        self._cachedarr = None
        return self

    def clear(self):
        self._op = None
        self._cachedarr = None
    def cleared(self) -> 'Window':
        self._op = None
        self._cachedarr = None
        return self

    def rend(self):
        """
        Render the entire screen.
        """
        sdl2.SDL_UpdateTexture(
            self._texture,
            None,
            self._arr.ctypes.data,
            self._sze[0]*4
        )

        sdl2.SDL_RenderCopy(self._renderer, self._texture, None, None)
        sdl2.SDL_RenderPresent(self._renderer)

    def set_title(self, title: str):
        """
        Set the title of the window

        Args:
            title (str): The new title of the window
        """
        sdl2.SDL_SetWindowTitle(self._mainWin, title.encode("utf-8"))
    def set_icon(self, icon: Surface):
        pass # TODO: This
        #icon = sdlimage.IMG_Load(b"icon.png")
        #sdl2.SDL_SetWindowIcon(window, icon)
        #sdl2.SDL_FreeSurface(icon)

    def toSurf(self) -> Surface:
        return Surface(self._arr)

    def getOp(self) -> base.Op | None:
        return self._op

    def copy(self) -> 'Window':
        new = Window(self._sze)
        new.isSmooth = self.isSmooth
        if self._op is not None:
            new._op = copy.copy(self._op)
        if self._cachedarr is not None:
            new._cachedarr = self._cachedarr.copy()
        return new

