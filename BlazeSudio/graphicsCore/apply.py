from BlazeSudio.graphicsCore import base
import numpy as np
import pygame

__all__ = ['Apply']

class Apply:
    _ops: list[base.Op] # Change from list to np.array
    _WinSur: bool

    def __call__(self) -> pygame.Surface:
        # Get all the elements, applying the operations on them, additionally finding the output size
        elms: list[base.ElmOp] = []
        sze = (0, 0)
        for op in self._ops:
            opTyp = op.typ
            if opTyp == base.OpsList.Size:
                sze = op.sze
            if op.isElm:
                elms.append(op)
            else:
                rms = []
                for idx, elm in enumerate(elms):
                    res = elm.Apply(op)
                    if not res:
                        rms.append(idx)
                for idx in rms:
                    elms.pop(idx)
        
        # If is the screen, make pygame resize to the new size
        if self._WinSur:
            sze = (sze[0], sze[1])
            if sze != pygame.display.get_window_size():
                pygame.display.set_mode(sze)
                if sze == (0, 0):
                    if not pygame.display.is_fullscreen():
                        pygame.display.toggle_fullscreen()
                elif pygame.display.is_fullscreen():
                    pygame.display.toggle_fullscreen()
        
        # Make the output screen and append all the elements
        if elms[0].typ == base.OpsList.Fill:
            arr = np.full((sze[1], sze[0]), elms.pop(0).col, np.uint32)
        else:
            arr = np.zeros((sze[1], sze[0]), np.uint32)
        
        for e in elms:
            e.ApplyOnArr(arr)
        
        # Turn the array into a pygame surface, first by converting to rgb
        h, w = arr.shape
        rgb_arr = np.zeros((h, w, 3), dtype=np.uint8)
        rgb_arr[:, :, 0] = (arr >> 16) & 0xFF  # Red
        rgb_arr[:, :, 1] = (arr >> 8) & 0xFF   # Green
        rgb_arr[:, :, 2] = arr & 0xFF          # Blue

        return pygame.surfarray.make_surface(rgb_arr.swapaxes(0, 1))
