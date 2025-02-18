import pygame

from BlazeSudio.graphics import stuff as GS
from BlazeSudio.graphics import options as GO
from BlazeSudio.graphics import stacks as STACKS
from BlazeSudio.graphics import GUI, mouse
from BlazeSudio.graphics.base import Element


# TODO: make initial creation of elements faster

# Graphics elements # TODO:
# [ ] Checkbox
# [ ] Slider / progressbar (combine into one)
# [ ] Tabbed layout
# [ ] Any sort of layout, really (Just use things like scrollables) (Maybe in a new file)
# [ ] Everything in Gradio

__all__ = ['Screen', 'RunInstantly']

class Screen(GUI.GraphicBase):
    # Things you *can* modify, but need to use `super()`
    def __init__(self, bgcol: GO.C___ = GO.CWHITE, maxFPS: int | None = 60, win: pygame.Surface = None):
        """
        The class for making really cool graphic screens :)

        To extend this function in sub-classes (highly recommended, even if it's to leave it blank), you should use `super().__init__()` in your function somewhere.

        Args:
            bgcol (tuple[int, int, int] | GO.C___, optional): _description_. Defaults to GO.CWHITE.
            maxFPS (int | None, optional): The maximum FPS the screen should run at. Defaults to 60.
            win (pygame.Surface, optional): \
                **IF YOU DO NOT SPECIFY:** If you have already made a pygame window it finds that and prints to that. \
                **IF YOU SPECIFY A SURFACE:** Instead of printing to the screen it prints to the surface. *Defaults to None.*
        """
        if win is None:
            if pygame.display.get_active():
                self.WIN = pygame.display.get_surface()
            else:
                self.WIN = pygame.display.set_mode(flags=pygame.NOFRAME | pygame.FULLSCREEN)
        else:
            self.WIN = win
        self.bgcol = bgcol
        self.clock = pygame.time.Clock()
        self.stacks = STACKS.Stack()
        self.Stuff = GS.Collection(self)
        self.run = False
        self.rel = False
        self.pause = False

        self.maxFPS = maxFPS
    
    @property
    def deltaTime(self):
        """
        The time between the last frame and the current frame in seconds.
        """
        return self.clock.get_time() / 1000
    
    def __call__(self):
        """
        This is how you should run your graphics screen. If you are to override this function in sub-classes, you should use `return super().__call__()` in your function somewhere.
        """
        return self.__run()
    
    # Things you can modify
    def _LoadUI(self):
        """
        Every time it loads the UI (first, or when `self.Reload()` is ran) it calls this function. This function will always be called after `self.Clear()`.

        This function's purpose is to load all the elements onto the screen.
        """
        pass

    def _ElementClick(self, obj: Element):
        """
        This function is called every time an element is clicked.

        Args:
            obj (GUI.base.Element): The element that was clicked.
        """
        pass

    def _Tick(self):
        """
        This function is called every tick of the game before everything else has even thought about going.
        This is used to draw things behind all the other GUI elements or to do stuff that influences elements.
        """
        pass

    def _Event(self, event: pygame.event.Event):
        """
        When a pygame event occurs (click mouse, press button, etc.)

        Args:
            event (pygame.event.Event): The event that was called.
        """
        pass

    def _DrawAft(self):
        """
        This function is called every time *just before* the screen is drawn. This could be used for things to be drawn on top of all the other GUI elements.
        To draw something *behind* the other elements, use `_Tick()`.

        This function can also be used for events that happen after everything else.
        """
        pass

    def _Last(self, aborted: bool):
        """
        This function is called when the screen is about to close. What it returns the function will too.

        Args:
            aborted (bool): Whether the screen was aborted by something or not (i.e. the user clicked the X button).
        """
        pass

    def __str__(self):
        return '<A graphics Screen object>'
    
    # Things you CAN'T modify
    def __run(self):
        self.run = True
        self.rel = False
        self.pause = False
        self.Clear()
        self._LoadUI()
        while self.run:
            self.WIN.fill(self.bgcol)
            mouse.Mouse.set(mouse.MouseState.NORMAL)
            self._Tick()
            evs = pygame.event.get()
            for obj in self._updateStuff(GUI.MousePos(*pygame.mouse.get_pos()), evs.copy()):
                self._ElementClick(obj)
            mouse.Mouse.update()
            if self.rel:
                self.rel = False
                self.Clear()
                self._LoadUI()
            for event in evs:
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
                if not self.pause:
                    self._Event(event)
            self._DrawAft()
            pygame.display.flip()
            if self.maxFPS is not None:
                self.clock.tick(self.maxFPS)
        return self._Last(self.run is None)
    
    @property
    def size(self):
        return (self.WIN.get_width(), self.WIN.get_height()-sum(i.size[1] for i in self.Stuff.getall() if isinstance(i, GUI.TerminalBar)))
    @property
    def sizeOfScreen(self):
        return self.size
    
    def set_caption(self, caption: str = None, iconsur: pygame.Surface = None):
        """Sets the caption of the screen! Highly recommend to use at the start of your code.
        Also highly recommend that when you use this function you modify at least one thing as otherwise it is a waste of your time.

        Args
            caption (str, optional): The caption to display, by default this is not modified.
            iconsur (pygame.Surface, optional): The icon of the window, by default this is not modified.
        """
        if caption is not None:
            pygame.display.set_caption(caption)
        if iconsur is not None:
            pygame.display.set_icon(iconsur)
    
    def Reload(self):
        """
        Reloads the screen, removing all the current things and rerunning the LoadUI.
        
        You should not run this very often (only when changing a *lot* of things (like exiting from one screen and going into the next)), \
        because it is slow if you have many things to load. Instead, try `.set` on the elements you wish to update.
        """
        self.rel = True

    def Clear(self, ignores=[]):
        self.pause = False
        self.Stuff.clear(ignores)
        self.stacks.clear()
    
    def Abort(self):
        self.run = None
    
    def __repr__(self):
        return str(self)

class RunInstantly:
    """
    This class can be used in conjunction to the main `Screen` class to run the screen instantly.

    i.e.
    ```python
    class Test(Screen, RunInstantly):
        def __init__(self, *args):
            ...
            super().__init__()
        ...
    
    Test()
    ```
    """
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)
        instance.__call__()
        return instance
