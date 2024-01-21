import tkinter as tk
from threading import Thread

class overlayWIN(tk.Tk):
    def __init__(self):
        super().__init__()
        self._root().wm_attributes('-topmost', True) # Topmost
        # Hide title bar
        self._root().overrideredirect(1)
        self._root().update_idletasks()
        self._root().lift()
    
    def PSUpdate(self, size, pos): # Pos and Size Update
        self._root().geometry('%dx%d+%d+%d' % (*size, *pos))
    
    def destroy(self):
        '''Destroy this overlay'''
        super().destroy()
        del self
    
    def hide(self):
        '''Hide this overlay.'''
        self._root().withdraw()

    def show(self):
        '''Show this overlay.'''
        self._root().wm_deiconify()
        self._root().lift()
        self._root().wm_attributes('-topmost', True)

class Overlay:
    def __init__(self, size, pos):
        """
        Makes an overlay! Basically, a Tkinter window that sits on top of everything without a title bar!

        Parameters
        ----------
        size : tuple[int, int]
            The size of the bar, can be changed with `overlay.size = <tuple[int, int]>` (see below)
        pos : tuple[int, int]
            The position of the bar on the screen, can be changed with `overlay.pos = <tuple[int, int]>` (see below)
        
        # HOW TO USE:
        It automatically runs in the background!

        To update the position and size (if you changed it) you must run `overlay.update()`

        To destroy the window, run `overlay.destroy()`

        To hide/show the window use `overlay.hide()` or `overlay.show()`

        To add an element to it, do what you would usually do to a Tkinter window except call this class, e.g.
        `tk.Button(overlay(), text='hi!')`
        """
        self.size = size
        self.pos = pos
        self.thread = Thread(target=self._runloop, daemon=True, args=(self,))
        self.thread.start()
        inited = False
        while not inited:
            try:
                self.win
                inited = True
            except: pass
        self.update()
    
    def _runloop(threadself, self):
        self.win = overlayWIN()
        self.win.mainloop()
    
    def running(self):
        return self.thread.is_alive()
    
    def update(self):
        self.win.geometry('%dx%d+%d+%d' % (*self.size, *self.pos))
    
    def destroy(self):
        '''Destroy this overlay'''
        self.win.destroy()
    
    def hide(self):
        '''Hide this overlay.'''
        self.win.withdraw()

    def show(self):
        '''Show this overlay.'''
        self.win.wm_deiconify()
        self.win.lift()
        self.win.wm_attributes('-topmost', True)
    
    def __call__(self): return self.win
