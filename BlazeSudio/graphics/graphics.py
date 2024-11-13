import pygame

from BlazeSudio.graphics import stuff as GS
from BlazeSudio.graphics import options as GO
from BlazeSudio.graphics.loading import (
    LoadingDecorator, 
    Progressbar
)
from BlazeSudio.graphics import stacks as STACKS
from BlazeSudio.graphics import GUI, mouse


# TODO: make initial creation of elements faster

# Graphics elements # TODO:
# [ ] Checkbox
# [ ] Slider / progressbar (combine into one)
# [ ] Tabbed layout
# [ ] Any sort of layout, really (Just use things like scrollables) (Maybe in a new file)
# [ ] Everything in Gradio

class Graphic(GUI.GraphicBase):
    def __init__(self, bgcol: GO.C___ = GO.CWHITE, win: pygame.Surface = None):
        """
        The class for making really cool graphic screens :)

        Args:
            bgcol (tuple[int, int, int] | GO.C___, optional): _description_. Defaults to GO.CWHITE.
            win (pygame.Surface, optional): \
                **IF YOU DO NOT SPECIFY:** If you have already made a pygame window it finds that and prints to that. \
                **IF YOU SPECIFY A SURFACE:** Instead of printing to the screen it prints to the surface. *Defaults to None.*
        """
        if win is None:
            if pygame.display.get_active():
                self.WIN = pygame.display.get_surface()
            else:
                self.WIN = pygame.display.set_mode()
                pygame.display.toggle_fullscreen()
        else:
            self.WIN = win
        self.bgcol = bgcol
        self.clock = pygame.time.Clock()
        self.stacks = STACKS.Stack()
        self.Stuff = GS.Collection()
        self.store = {}
        self.rel = False
        self.ab = False
        self.pause = False
        self.callbacks = {}
        self.Container = GS.Container()
    
    @property
    def size(self):
        return (self.WIN.get_width(), self.WIN.get_height()-sum(i.size[1] for i in self.Stuff.getall() if isinstance(i, GUI.TerminalBar)))
    @property
    def sizeOfScreen(self):
        return self.size
    
    def set_caption(self, caption=None, iconsur=None):
        """Sets the caption of the screen! Highly recommend to use at the start of your code.
        Also highly recommend that when you use this function you modify at least one thing as otherwise it is a waste of your time.

        Args
            caption (str, optional): The caption to display, by default this is not modified
            iconsur (pygame.Surface, optional): The icon of the window, by default this is not modified
        """
        if caption is not None:
            pygame.display.set_caption(caption)
        if iconsur is not None:
            pygame.display.set_icon(iconsur)
    
    def Loading(self, func):
        """
        @G.Loading
        Makes a Loading screen while you do a function!
        """
        def func2():
            return LoadingDecorator(func)(self.WIN, GO.FTITLE)
        return func2
    
    def PBLoading(self, tasks, loadingtxt='Loading{3} {2}% ({0} / {1})'):
        """Have a loading screen! Like G.Loading, but with a progressbar!

        Parameters
        ----------
        tasks : list[async functions]
            The list of async functions to run.
        loadingtxt : str, optional
            The text to display on the loading screen, by default 'Loading{3} {2}% ({0} / {1})'
            {0}: Amount of tasks completed
            {1}: Amount of tasks
            {2}: % complete
            {3}: ... (i.e. the dots change every 3rd of a second from . to .. to ... and back)

        Returns
        -------
        tuple[Progressbar, function]
            The Progressbar object and the function which runs the progressbar
            Call `function()` to run the progressbar.
            The function will return the output list of all the return values of each of the functions inputted
            But if you quit the loading then the function will return None
        """
        self.WIN.fill(GO.CWHITE)
        pygame.display.update()
        pbar = Progressbar(600, 50)
        res = pbar(self.WIN, (self.size[0] - 600) // 2, (self.size[1] - 50) // 2, 5, tasks, loadingtxt)
        return pbar, res

    def Catch(self, func):
        """
        @G.Catch
        A function decorator to run the function, but if it encounters any errors it will \
spawn up another Graphic screen allowing you to go back to the previous screen, or raise it for debugging.
        """
        def func2(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                @self.Graphic
                def errored(event, *args, element=None, aborted=False, **kwargs):
                    if event == GO.ELOADUI:
                        nonlocal e
                        self.Clear()
                        self.add_text('AN EXCEPTION OCCURED!', GO.CRED, GO.PCTOP, GO.FTITLE)
                        self.add_text(str(type(e)), GO.CRED, GO.PCTOP, GO.FTITLE)
                        self.add_text(str(e), GO.CGREY, GO.PCCENTER, GO.FCODEFONT)
                        def rse(_):
                            self.run = False # Quit without aborting
                        self.add_button('Back', GO.CGREEN, GO.PCBOTTOM, callback=rse)
                        self.add_button('Raise exception', GO.CRED, GO.PRBOTTOM, callback=lambda _: self.Abort())
                    elif event == GO.ELAST:
                        return aborted
                if errored():
                    raise e
        return func2
    
    def Screen(self, funcy, /, *, events=pygame.event.get, mousepos=pygame.mouse.get_pos):
        """
        Usages:
        ```python
        @G.Screen # OR @G.Screen(**options)
        def func(event, *args, element=None, aborted=False, **kwargs):
            ...

        ```

        Makes a Graphic Screen!
        TODO: Add more options for here

        Parameters
        ----------
        funcy : function
            The function to wrap
        slf : class object, optional
            The class to pass to all the function calls if any, by default None
        generator : bool, optional
            Whether or not this function is a generator, by default False
        update : bool, optional
            Whether or not to update the screen, by default True
            This may be false if for example something else updates the screen too and you don't want that flickering
        events : function, optional
            The function to call to get all the current events, by default pygame.event.get
        mousepos : function, optional
            The function to call to get the current mouse position, by default pygame.mouse.get_pos
        """
        def func2(*args, **kwargs):
            stuff = self.Stuff.copy()
            prevstack = self.stacks.copy()
            prevPause = self.pause
            self.Stuff.clear()
            self.stacks.clear()
            def func(event, element=None, aborted=False):
                if event == GO.EELEMENTCLICK and element in self.callbacks:
                    ret = self.callbacks[element](element)
                ret = funcy(event, *args, element=element, aborted=aborted, **kwargs)
                return ret
            cont = self.Container.copy()
            func(GO.EFIRST)
            self.run = True
            self.ab = False
            self.rel = False
            func(GO.ELOADUI)
            while self.run and not self.ab:
                evnts = events()
                self.WIN.fill(self.bgcol)
                mouse.Mouse.set(mouse.MouseState.NORMAL)
                for obj in self._updateStuff(mousepos(), evnts):
                    func(GO.EELEMENTCLICK, obj)
                mouse.Mouse.update()
                if self.rel:
                    self.rel = False
                    self.Stuff.clear()
                    func(GO.ELOADUI)
                if func(GO.ETICK) is False:
                    self.run = False
                for event in evnts.copy():
                    if event.type == pygame.QUIT:
                        self.run = False
                    if not self.pause:
                        func(GO.EEVENT, event)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.run = False
                pygame.display.flip()
                self.clock.tick(60)
            ret = func(GO.ELAST, aborted=self.ab)
            # Reset back to whatever it was before
            self.Container = cont
            self.ab = False
            self.run = True
            self.stacks.replaceWith(prevstack)
            self.Stuff.clear()
            self.Stuff = stuff
            self.pause = prevPause
            return ret
        
        return func2
    
    def Reload(self):
        """
        Reloads the screen, removing all the current things and rerunning the ELOADUI for the current function.
        
        You should not run this very often (only when changing a *lot* of things (like exiting from one screen and going into the next)), \
because it is slow if you have many things to load. Instead, try `.set` on the elements you wish to update.
        """
        self.rel = True
    
    def Clear(self, ignores=[]):
        self.store = {}
        self.pause = False
        self.callbacks = {}
        self.Stuff.clear(ignores)
        self.stacks.clear()
    
    def Abort(self, *args):
        self.ab = True
