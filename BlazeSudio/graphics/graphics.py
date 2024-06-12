from copy import copy
import pygame
pygame.init()

from BlazeSudio.graphics import stuff as GS
from BlazeSudio.graphics import options as GO
from BlazeSudio.graphics.loading import (
    LoadingDecorator, 
    IsLoading, 
    Progressbar
)
from BlazeSudio.graphics import stacks as STACKS
import BlazeSudio.graphics.GUI.elements as GUI
from BlazeSudio.graphics.GUI import ColourPickerBTN, dropdown, Toast
from BlazeSudio.graphics.GUI.textboxify.borders import LIGHT

# TODO: make initial creation of elements faster

# Graphics elements # TODO:
# [ ] Checkbox
# [ ] Slider / progressbar (combine into one)
# [ ] Tabbed layout
# [ ] Any sort of layout, really (Just use things like scrollables) (Maybe in a new file)

class GScrollable(GUI.Scrollable):
    def __init__(self, G, pos, goalrect, sizeOfScreen, outline, bar):
        super().__init__(G, pos, goalrect, (0, sizeOfScreen[1]-goalrect[1]), outline, bar)
        self.events = []
        s = pygame.Surface(sizeOfScreen)
        self.newG = Graphic(win=s, TB=False, no_id=True)
        def func(event, *_, aborted=True, **__):
            if event == GO.ETICK: return True
            elif event == GO.EELEMENTCLICK: return
            return aborted
        self.GR = self.newG.Graphic(func, generator=True, update=False, events=self.getevents, mousepos=self.getmouse)()
    
    def get(self):
        """Get the Graphic in the scrollable"""
        return self.newG
    
    def update(self, mousePos, events):
        self.newG.pause = self.G.pause
        
        self.events = events
        r = next(self.GR)
        self.sur = self.newG.WIN
        super().update(mousePos, events)
        if r != None:
            if r[0]:
                self.Abort()
            else:
                self.run = False
    
    def getevents(self):
        for i in self.events:
            try:
                i.pos = self.getmouse()
            except: pass
        return self.events
    
    def getmouse(self):
        p = pygame.mouse.get_pos() # TODO: add support for Scrollables in Scrollables by changing this line
        x, y = self.stackP()
        np = (p[0]-x, p[1]-y-self.scroll)
        if np[0] > self.size[0] or p[1]-y > self.size[1]: return (float('-inf'), float('-inf'))
        return np

class TerminalBar:
    def __init__(self, win, spacing=5):
        self.win = win
        self.spacing = spacing
        self.active = -1
        self.txt = ''
    def pressed(self, event):
        if event.key == pygame.K_RETURN:
            pass
        elif event.key == pygame.K_BACKSPACE:
            self.txt = self.txt[:-1]
        else:
            self.txt += event.unicode
    def toggleactive(self, forceactive=None):
        if forceactive != None:
            if forceactive: self.active = 60
            else: self.active = -1
        if self.active == -1: self.active = 60
        else: self.active = -1
    def update(self):
        t = '>/'+self.txt
        if self.active >= 30: t += '_'
        if self.active >= 0:
            self.active -= 1
            if self.active <= 0: self.active = 60
        r = GO.FCODEFONT.render(t, GO.CWHITE)
        h = r.get_height()+self.spacing*2
        pygame.draw.rect(self.win, GO.CBLACK, pygame.Rect(0, self.win.get_height()-h, self.win.get_width(), h))
        self.win.blit(r, (self.spacing, self.win.get_height()-h+self.spacing))
    def collides(self, x, y):
        r = GO.FCODEFONT.render('>/', GO.CWHITE)
        h = r.get_height()+self.spacing*2
        return pygame.Rect(0, self.win.get_height()-h, self.win.get_width(), h).collidepoint(x, y)

class GraphicInfo:
    NUMGRAPHICSS = 0
    GRAPHICSPROCESSES = {}
    RUNNINGGRAPHIC = (None, None)

class CustomGraphic: # This is if you don't want to use the actual graphics library and just want to use your own stuff
    # TODO: Remove this class
    def __init__(self, win):
        self.WIN = win
        self.pause = False

class Graphic:
    def __init__(self, bgcol=GO.CWHITE, TB=True, win=None, no_id=False):
        """The class for making really cool graphic screens :)

        Parameters
        ----------
        bgcol : tuple[int, int, int]
            The colour of the button. For ease of use default colours are provided as GO.C___ (e.g. GO.CGREEN)
        TB : bool, optional
            Whether or not you want the little terminal bar at the bottom, by default True
        win : pygame.Surface, optional
            IF YOU DO NOT SPECIFY: If you have already made a pygame window it finds that and prints to that
            IF YOU SPECIFY A SURFACE: Instead of printing to the screen it prints to the surface
        no_id : int, optional
            DO NOT USE THIS UNLESS THIS GRAPHIC IS INSIDE ANOTHER GRAPHIC IN WHICH CASE DO USE THIS
            If it is True then it may run multiple graphics windows at a time depending on your code
            If it is False then only one graphic window can be open at a time
            Defaults to False
        """
        if win == None:
            if pygame.display.get_active():
                self.WIN = pygame.display.get_surface()
            else:
                self.WIN = pygame.display.set_mode()
                pygame.display.toggle_fullscreen()
        else: self.WIN = win
        if TB:
            self.TB = TerminalBar(self.WIN)
            self.size = (self.WIN.get_width(), self.WIN.get_height()-26)
        else:
            class FakeTB:
                toggleactive = lambda *args: False
                collides = lambda *args: False
                update = lambda *args: None
                active = -1
            self.TB = FakeTB()
            self.size = self.WIN.get_size()
        if no_id:
            self.id = None
        else:
            self.id = GraphicInfo.NUMGRAPHICSS
            GraphicInfo.NUMGRAPHICSS += 1
            GraphicInfo.GRAPHICSPROCESSES[self.id] = 0
        self.bgcol = bgcol
        self.clock = pygame.time.Clock()
        self.stacks = STACKS.Stack()
        self.Stuff = GS.Collection()
        # Watch is for elements that should always exist
        self.Stuff.watch.add_many((
            'buttons',
            'text',
            'surs',
            'switches',
            'customs',
            'input_boxes',
            'scrollsables',
            'cps', # ColourPickerS
            'Empties',
        ))
        # Sprites are for things that may get deleted and nothing should happen because of it
        self.Stuff.sprites.add_many((
            'toasts',
            'TextBoxes',
        ))
        self.store = {}
        self.rel = False
        self.ab = False
        self.pause = False
        self.callbacks = {}
        self.Container = GS.Container()
    def set_caption(self, caption=None, iconsur=None):
        """Sets the caption of the screen! Highly recommend to use at the start of your code.
        Also highly recommend that when you use this function you modify at least one thing as otherwise it is a waste of your time.

        Parameters
        ----------
        caption : str, optional
            The caption to display, by default this is not modified
        iconsur : pygame.Surface, optional
            The icon of the window, by default this is not modified
        """
        if caption != None: pygame.display.set_caption(caption)
        if iconsur != None: pygame.display.set_icon(iconsur)
    
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
    
    def CGraphic(self, funcy):
        """
        @G.CGraphic
        Passes a class to a Graphic screen!
        This can also be done with `G.Graphic(self)`
        """
        def func2(slf, *args, **kwargs):
            self.Graphic(funcy, slf)(*args, **kwargs)
        return func2
    
    def Graphic(self, funcy, slf=None, /, *, generator=False, update=True, events=pygame.event.get, mousepos=pygame.mouse.get_pos):
        """
        @G.Graphic
        @G.Graphic(slf=None, **options)
        Makes a Graphic class!
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
            prev = GraphicInfo.RUNNINGGRAPHIC
            if self.id is None:
                idx = None
            else:
                idx = GraphicInfo.GRAPHICSPROCESSES[self.id]
                GraphicInfo.GRAPHICSPROCESSES[self.id] += 1
                GraphicInfo.RUNNINGGRAPHIC = (self.id, idx)
            def func(event, element=None, aborted=False):
                pidx = GO.PIDX
                if event == GO.EELEMENTCLICK and element in self.callbacks:
                    ret = self.callbacks[element](element)
                if slf == None:
                    ret = funcy(event, *args, element=element, aborted=aborted, **kwargs)
                else:
                    ret = funcy(slf, event, *args, element=element, aborted=aborted, **kwargs)
                if self.id is not None:
                    GraphicInfo.RUNNINGGRAPHIC = (self.id, idx)
                GO.PIDX = pidx
                return ret
            cont = copy(self.Container)
            func(GO.EFIRST)
            self.run = True
            self.ab = False
            self.rel = True
            func(GO.ELOADUI)
            while self.run and not self.ab:
                while IsLoading[0] or (self.id is not None and GraphicInfo.RUNNINGGRAPHIC != (self.id, idx)):
                    pass # DO NOT DO ANYTHING while loading or having multiple graphic screens open at a time
                evnts = events()
                self.WIN.fill(self.bgcol)
                returns = self.Stuff.update(mousepos(), evnts.copy())
                blocked = False
                for obj in returns:
                    retValue = returns[obj]
                    if retValue is None:
                        continue
                    
                    for ret in retValue.get():
                        if ret == GUI.ReturnState.ABORT:
                            self.Abort()
                        elif ret == GUI.ReturnState.CALL:
                            r = func(GO.EELEMENTCLICK, obj)
                            if r != None:
                                self.run = False
                                yield [r]
                        elif ret == GUI.ReturnState.TBUTTON:
                            obj.update(mousepos(), evnts.copy(), True) # Redraw forcefully on top of everything else
                #if self.Stuff.diff() or self.rel: # TODO: remove
                #    self.rel = False
                #    func(GO.ELOADUI)
                self.TB.update()
                if func(GO.ETICK) is False:
                    self.run = False
                for event in evnts.copy():
                    if event.type == pygame.QUIT:
                        self.run = False
                    if not self.pause and not blocked:
                        func(GO.EEVENT, event)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.run = False
                        elif self.TB.active != -1:
                            self.TB.pressed(event)
                            blocked = True
                        # TODO: Integrate with textbox class
                        # if event.key == pygame.K_RETURN and self.TB.active == -1 and not any([i.active for i in self.Stuff['input_boxes']]):
                        #     for sprite in self.Stuff['TextBoxes']:
                        #         if sprite.words:
                        #             sprite.reset()
                        #         else:
                        #             func(GO.EELEMENTCLICK, Element(GO.TTEXTBOX, self.uids.index(sprite), self, sprite=sprite))
                        #     if len(self.Stuff['TextBoxes']) == 0:
                        #         self.pause = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and not self.pause:
                        if event.button == pygame.BUTTON_LEFT:
                            self.TB.toggleactive(not self.TB.collides(*mousepos()))
                yield None
                if update:
                    pygame.display.flip()
                    self.clock.tick(60)
            ret = func(GO.ELAST, aborted=self.ab)
            self.Container = cont # Reset back to whatever it was before
            GraphicInfo.RUNNINGGRAPHIC = prev # Give back the permission to go to the previous graphic screen
            self.ab = False
            self.run = True
            self.Stuff = stuff
            yield [ret]
        def func3(*args, **kwargs):
            f = func2(*args, **kwargs)
            while True:
                y = next(f)
                if y != None:
                    return y[0]
        if generator: return func2
        else: return func3

    def Toast(self, text, timeout=120, pos=GO.PCBOTTOM, dist=20, spacing=5, font=GO.FFONT, col=GO.CACTIVE, txtcol=GO.CWHITE):
        """
        Makes a toast!

        Parameters
        ----------
        text : str
            The text that is in the toast
        timeout : int, optional
            The time (in frames, 60 FPS) that the toast should remain on the screen for
        pos : GO.P___ (e.g. GO.PRBOTTOM), optional
            The position of the toast, by default GO.PCBOTTOM
        dist : int, optional
            The distance from `position` to the toast, by default 20
            For GO.PCCENTER this should be 0
            This means that you can have the toast 20 pixels off the bottom of the screen if you 
            have pos=GO.PCBOTTOM and dist=20
        spacing : int, optional
            The spacing from the edge of the bubble the toast is in to the text, by default 5
        font : GO.FNEW, optional
            The font of the text, by default GO.FFONT (other fonts provided as GO.F___)
        col : tuple[int, int, int], optional
            The colour of the toast, by default GO.CACTIVE (other colours provided as GO.C___)
        txtcol : tuple[int, int, int], optional
            The colour of the text, by default GO.CWHITE
        
        Returns
        -------
            Element: The created element
        """
        
        txt = font.render(text, txtcol)
        sur = pygame.Surface((txt.get_size()[0]+spacing*2, txt.get_size()[1]+spacing*2))
        sur.fill((255, 255, 255, 1))
        pygame.draw.rect(sur, col, sur.get_rect(), border_radius=spacing)
        sur.blit(txt, (spacing, spacing))

        t = Toast(self, pos, sur, dist, timeout)
        self.Stuff['toasts'].append(t)
        return t

    def Dropdown(self, elements, spacing=5, font=GO.FFONT, activecol=GO.CACTIVE, bgcol=GO.CBLACK, txtcol=GO.CWHITE, pos=None):
        """Spawns a GUI.dropdown!
        This will pause everything else! You will need to click out of the GUI.dropdown to exit it.

        Parameters
        ----------
        elements : list
            The choices that you can select
        spacing : int, optional
            The spacing between each element, by default 5
        font : GO.FNEW, optional
            The font of the text. For ease of use default fonts are provided as GO.F___ (e.g. GO.FCODEFONT), by default GO.FFONT
        activecol : tuple[int, int, int], optional
            The colour when you hover your mouse over an option, by default GO.CACTIVE
        bgcol : tuple[int, int, int], optional
            The colour of the background of the GUI.dropdown, by default GO.CBLACK
        txtcol : tuple[int, int, int], optional
            The colour of the text of the GUI.dropdown, by default GO.CWHITE
        pos : tuple[int, int], optional
            The position of the GUI.dropdown, by default the mouse location
        For ease of use default colours are provided as GO.C___ (e.g. GO.CGREEN)

        Returns
        -------
        int/None/False
            The index of the input elements list that was selected, else None if nothing selected
            False if you exited from the menu using escape or closing the window. This will also exit the GUI.
        """
        d = dropdown(self, elements, spacing, font, bgcol, txtcol, activecol, pos)
        if d is False:
            self.run = False
        return d
    
    def add_custom(self, sprite):
        """
        Adds a custom sprite to the screen!

        Parameters
        ----------
        sprite : Any
            The sprite to add!
        
        The sprite MUST have an `update` function which takes in 2 arguments: the current mouse position, and then the current events.
        """
        self.Stuff['customs'].append(sprite)
    
    def add_text(self, txt, colour, position, font=GO.FFONT, allowed_width=900):
        """Adds text to the GUI!

        Parameters
        ----------
        txt : str
            The text that will be added to the GUI.
        colour : tuple[int, int, int]
            The colour of the button. For ease of use default colours are provided as GO.C___ (e.g. GO.CGREEN)
        position : GO.P___ (e.g. GO.PRBOTTOM)
            The position on the screen this element will be placed
        font : GO.FNEW, optional
            The font of the text. For ease of use default fonts are provided as GO.F___ (e.g. GO.FCODEFONT), by default GO.FFONT
        allowed_width : int, optional
            The allowed width of the font, by default 900
        
        Returns
        -------
            Element: The created element
        """
        func = lambda t: font.render(t, colour, allowed_width=allowed_width) # TODO: Remove this and implement it in the text class itself
        obj = func(txt)
        t = GUI.Text(self, position, func, txt)
        self.Stuff['text'].append(t)
        return t
    
    def add_surface(self, obj, position):
        """Adds a surface to the GUI!

        Parameters
        ----------
        obj : pygame.Surface
            The surface to add to the screen!
        position : GO.P___ (e.g. GO.PRBOTTOM)
            The position on the screen this element will be placed
        
        Returns
        -------
            Element: The created element
        """
        s = GUI.Static(self, position, obj)
        self.Stuff['surs'].append(s)
        return s
    
    def add_empty_space(self, position, wid, hei):
        """Makes a piece of empty space.

        Parameters
        ----------
        position : GO.P___ (e.g. GO.PRBOTTOM)
            The position on the screen this element will be placed
            This is VERY IMPORTANT as the ONLY use of this element is when there is a stack, so you can push the stack in a direction with this.
        wid : int
            The width of the empty space (can be negative to push the elements back)
        hei : int
            The height of the empty space (can be negative to push the elements back)
        
        Returns
        -------
            Element: The created element (which is the blank space)
        """
        space = GUI.Empty(self, position, (wid, hei))
        self.Stuff['Empties'].append(space)
        return space
    
    def add_button(self, txt, col, position, txtcol=GO.CBLACK, font=GO.FFONT, allowed_width=900, on_hover_enlarge=True, callback=None):
        """Adds a button to the GUI!

        Parameters
        ----------
        txt : str
            The text ON the button
        col : tuple[int, int, int]
            The colour of the button. For ease of use default colours are provided as GO.C___ (e.g. GO.CGREEN)
        position : GO.P___ (e.g. GO.PRBOTTOM)
            The position on the screen this element will be placed
        txtcol : tuple[int, int, int], optional
            The colour of the text. For ease of use default colours are provided as GO.C___ (e.g. GO.CGREEN), by default GO.CBLACK
        font : GO.FNEW, optional
            The font of the text. For ease of use default fonts are provided as GO.F___ (e.g. GO.FCODEFONT), by default GO.FFONT
        allowed_width : int, optional
            The allowed_width of the font, by default 900
        on_hover_enlarge : bool/int, optional
            Whether to enlarge the button on hover. If this is an int it will be used as the size increase of said button. By default True
        callback : function(Element), optional
            The function to call when this element is pressed, by default None
            Please note that the main function will ALSO be called when this is pressed
        
        Returns
        -------
            Element: The created element
        """
        func = lambda t: font.render(t, txtcol, allowed_width=allowed_width)
        btn = GUI.Button(self, position, col, func, txt, (-1 if on_hover_enlarge==False else (10 if on_hover_enlarge==True else on_hover_enlarge)))
        self.Stuff['buttons'].append(btn)
        if callback != None:
            self.callbacks[btn] = callback
        return btn
    
    def add_TextBox(self, txt, position, border=LIGHT, indicator=None, portrait=None, callback=None):
        """Makes a new TextBox in the GUI!

        Parameters
        ----------
        txt : str
            The text to be displayed in the textbox.
        position : GO.P___ (e.g. GO.PRBOTTOM)
            The position on the screen this element will be placed
        border : graphics.GUI.textboxify.borders._____, optional
            The border to use on the textbox, by default LIGHT
        indicator : str, optional
            The path to the indicator file that will be used, by default None
        portrait : str, optional
            the path to the portrait file that will be used, by default None
        callback : function(Element), optional
            The function to call when this textbox is dismissed, by default None
            Please note that the main function will ALSO be called when this is dismissed
        
        Returns
        -------
            GUI.TextBoxFrame: The created element
        """
        dialog_box = GUI.TextBoxFrame( # TODO: Make more integrated with the rest of the graphics
            text=txt,
            text_width=320,
            lines=2,
            pos=(0, 0),
            padding=(150, 100),
            font_color=(92, 53, 102),
            font_size=26,
            bg_color=(173, 127, 168),
            border=border,
        )
        
        dialog_box.set_indicator(indicator)
        dialog_box.set_portrait(portrait)
        dialog_box.rect.topleft = position # TODO: Fix
        self.Stuff['TextBoxes'].append(dialog_box)
        self.pause = True
        if callback != None:
            self.callbacks[dialog_box] = callback
        return dialog_box
    
    def add_input(self, position, font=GO.FSMALL, width=None, resize=GO.RHEIGHT, placeholder='Type Here', maximum=100, start='', callback=None):
        """Adds an input box :)

        Parameters
        ----------
        position : GO.P___ (e.g. GO.PRBOTTOM)
            The position on the screen this element will be placed
        font : GO.FNEW, optional
            The font of the text. For ease of use default fonts are provided as GO.F___ (e.g. GO.FCODEFONT), by default GO.FFONT
        width : int, optional
            The width of the text box, by default the width of the placeholder text
            This is important as if the resize is height, it will wrap around this width. If the resize is width this doesn't matter.
        resize : GO.R___ (e.g. GO.RHEIGHT), optional
            The resize to use, by default GO.RHEIGHT
            This means that if you reach the end of the box it will either resize the box width ways or wrap the text around height
        placeholder : str, optional
            The text displayed if nothing is entered, by default 'Type Here'
        maximum : int, optional
            The maximum NUMBER OF CHARACTERS you can input, by default 100
            Make this None to have no limit
        start : str, optional
            The text that STARTS in the textbox, by default "" (the only way to see the placeholder text is with the text in the box as "")
        callback : function(Element), optional
            The function to call when you press enter while inputting into this element, by default None
            Please note that the main function will ALSO be called when you press enter while inputting into this element
        
        Returns
        -------
            Element: The created element
        """
        sze = list(font.winSze(placeholder))
        if maximum is None:
            maximum = sze+5
        if width is not None:
            sze[0] = width+5
        else:
            sze[0] += 5
        sze[1] += 10
        ibox = GUI.InputBox(self, position, sze, resize, placeholder, font, maximum, start) # TODO: Positioning and custom width & height & resize
        self.Stuff['input_boxes'].append(ibox)
        if callback != None:
            self.callbacks[ibox] = callback
        return ibox
    
    def add_num_input(self, position, font=GO.FSMALL, width=None, resize=GO.RHEIGHT, start=0, bounds=(float('-inf'), float('inf')), callback=None):
        """Adds an input box for numbers :)

        Parameters
        ----------
        position : GO.P___ (e.g. GO.PRBOTTOM)
            The position on the screen this element will be placed
        font : GO.FNEW, optional
            The font of the number. For ease of use default fonts are provided as GO.F___ (e.g. GO.FCODEFONT), by default GO.FFONT
        width : int, optional but recommended
            The amount of numbers wide the input box is, by default as wide as the 'start' input number
            This is important as if the resize is height, it will wrap around this width. If the resize is width this doesn't matter.
        resize : GO.R___ (e.g. GO.RHEIGHT), optional
            The resize to use, by default GO.RHEIGHT
            This means that if you reach the end of the box it will either resize the box width ways or wrap the text around height
        start : int, optional
            The starting number, by default 0
        bounds : tuple[int, int], optional
            The maximum and minimum number you can input, by default (-inf, inf)
        callback : function(Element), optional
            The function to call when you press enter while inputting into this element, by default None
            Please note that the main function will ALSO be called when you press enter while inputting into this element
        
        Returns
        -------
            Element: The created element
        """
        sze = list(font.winSze(str(start)))
        if width is not None:
            sze[0] = font.winSze('9'*width)[0]+5
        sze[0] += 5
        sze[1] += 10
        ibox = GUI.NumInputBox(self, position, sze, resize, start, *bounds, font) # TODO: Positioning and custom width & height & resize
        self.Stuff['input_boxes'].append(ibox)
        if callback != None:
            self.callbacks[ibox] = callback
        return ibox
    
    def add_switch(self, position, size=20, default=False, callback=None):
        """Adds a switch to the GUI! :)

        Parameters
        ----------
        position : GO.P___ (e.g. GO.PRBOTTOM)
            The position on the screen this element will be placed
        size : int, optional
            The size of the switch, by default 20
        default : bool, optional
            Whether the switch starts as on or off, by default False
        callback : function(Element), optional
            The function to call when this element is pressed, by default None
            Please note that the main function will ALSO be called when this is pressed
        
        Returns
        -------
            Element: The created element
        """
        sw = GUI.Switch(self, position, size, 2, default)
        self.Stuff['switches'].append(sw)
        if callback != None:
            self.callbacks[sw] = callback
        return sw

    def add_colour_pick(self, position, size=20, sow=200):
        """Adds a colour picker button to the GUI!
        This is like a button with a colour on it that when you press it you can change the colour

        Parameters
        ----------
        position : GO.P___ (e.g. GO.PRBOTTOM)
            The position on the screen this element will be placed
        size : int, optional
            The size of the colour picker button, by default 20
        sow : int, optional
            The size of the colour picker window, by default 200
        
        Returns
        -------
            Element: The created element
        """
        btn = ColourPickerBTN(self, position, size, sow)
        self.Stuff['cps'].append(btn)
        return btn
    
    def add_Scrollable(self, position, size, sos, outline=10, bar=True):
        """Adds a GUI.Scrollable window to the Graphic screen!
        This is like another really tiny Graphic screen inside the big one, but the tiny one you can scroll!

        Parameters
        ----------
        position : GO.P___ (e.g. GO.PRBOTTOM)
            The position on the screen this element will be placed
        size : tuple[int, int]
            The size of the scrollable box
        sos : tuple[int, int]
            The size of the screen (How big the created tiny Graphic screen will be)
            If this is > size you can scroll through it
            Currently only works for horizontal scrolling
        outline : int, optional
            The thickness of the outline, 0 to turn it off, by default 10
        bar : bool, optional
            Whether or not to have a little red scrollbar in the side, by default True
            The thickness of the scrollbar is constant (10)

        Returns
        -------
        tuple[Graphic, Element]
            (The Graphic class created which is put onto the main one, the Element which is the new scrollable)
        """
        s = GScrollable(self, position, size, sos, outline, bar)
        self.Stuff['scrollsables'].append(s)
        return s.newG, s
    
    def Reload(self):
        """
        Reloads the screen, removing all the current things and rerunning the ELOADUI for the current function.
        
        This is ill-advised, because it is slow if you have many things to load. Instead, try `.set` on the elements you wish to update.
        """
        self.rel = True
    
    def Clear(self):
        GO.PIDX = 0
        self.store = {}
        self.pause = False
        self.callbacks = {}
        self.Stuff.clear()
        self.stacks.clear()
    
    def Abort(self, *args):
        self.ab = True
