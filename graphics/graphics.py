import pygame, asyncio
pygame.init()
import graphics.graphics_options as GO
from graphics.loading import Loading
from graphics.async_handling import Progressbar
from graphics.GUI import (
    TextBoxFrame, 
    InputBox, 
    Button, 
    Switch, 
    dropdown, 
    NumInputBox, 
    Scrollable, 
    ColourPickerBTN, 
    Toast,
)
from graphics.GUI.textboxify.borders import LIGHT

class GScrollable(Scrollable):
    def __init__(self, WIN, pos, goalrect, sizeOfScreen, outline, bar):
        self.WIN = WIN
        self.pos = pos
        self.goalrect = goalrect
        self.events = []
        s = pygame.Surface(sizeOfScreen)
        self.G = Graphic(win=s, TB=False)
        def func(event, *args, aborted=True, **kwargs):
            if event == GO.ETICK: return True
            elif event == GO.EELEMENTCLICK: return
            return aborted
        self.GR = self.G.Graphic(func, generator=True, update=False, events=self.getevents, mousepos=self.getmouse)()
        super().__init__(self.G.WIN, pos, goalrect, (0, sizeOfScreen[1]-goalrect[1]), outline, bar)
    
    def getevents(self):
        for i in self.events:
            try:
                i.pos = self.getmouse()
            except: pass
        return self.events
    def getmouse(self):
        p = pygame.mouse.get_pos()
        np = (p[0]-self.pos[0], p[1]-self.pos[1]-self.scroll)
        if np[0] > self.goalrect[0] or p[1]-self.pos[1] > self.goalrect[1]: return (float('-inf'), float('-inf'))
        return np
    
    def __call__(self, events):
        self.events = events
        r = next(self.GR)
        self.sur = self.G.WIN
        super().__call__(self.WIN)
        if r != None: return r
        return False

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
        r = GO.FCODEFONT.render(t, 1, GO.CWHITE)
        h = r.get_height()+self.spacing*2
        pygame.draw.rect(self.win, GO.CBLACK, pygame.Rect(0, self.win.get_height()-h, self.win.get_width(), h))
        self.win.blit(r, (self.spacing, self.win.get_height()-h+self.spacing))
    def collides(self, x, y):
        r = GO.FCODEFONT.render('>/', 1, GO.CWHITE)
        h = r.get_height()+self.spacing*2
        return pygame.Rect(0, self.win.get_height()-h, self.win.get_width(), h).collidepoint(x, y)

class Element:
    def __init__(self, typ, uid, G, **kwargs):
        if typ not in [getattr(GO, i) for i in dir(GO) if i.startswith('T')]:
            raise TypeError(
                f'Input \'type\' MUST be GO.T___ (e.g. GO.TBUTTON), not {str(typ)}!'
            )
        self.uid = uid
        self.name = [i for i in dir(GO) if i.startswith('T')][[getattr(GO, i) for i in dir(GO) if i.startswith('T')].index(typ)]
        self.type = typ
        self.G = G
        try:
            if self.type == GO.TBUTTON:
                self.btn = kwargs['btn']
                self.txt = self.btn[0][0][0]
            elif self.type == GO.TTEXTBOX:
                self.sprite = kwargs['sprite']
            elif self.type == GO.TINPUTBOX:
                self.sprite = kwargs['sprite']
                self.txt = kwargs['txt']
            elif self.type == GO.TSWITCH:
                self.sprite = kwargs['sw']
        except KeyError as e:
            raise TypeError(
                f'{self.name} Element requires kwarg "{str(e)}" but was not provided!'
            )
    
    def remove(self):
        """Removes an element.

        Only works on:
         - GO.TTEXTBOX
         - GO.TINPUTBOX
         - GO.TSWITCH
        """
        if self.type == GO.TTEXTBOX:
            self.G.sprites.remove(self.sprite)
        elif self.type == GO.TINPUTBOX:
            self.G.input_boxes.remove(self.sprite)
        elif self.type == GO.TSWITCH:
            self.G.sprites.remove(self.sprite)
        else:
            raise NotImplementedError(
                f'Remove has not been implemented for this element with type {self.name}!'
            )
    
    def set_text(self, txt):
        """Sets text of an element.

        Only works on:
         - GO.TTEXTBOX (A TextBox element)
         
        Parameters:
        txt : str
        """
        if self.type == GO.TTEXTBOX:
            self.sprite.reset(hard=True)
            self.sprite.set_text(txt)
        else:
            raise NotImplementedError(
                f'Set text has not been implemented for this element with type {self.name}!'
            )
    
    def get(self):
        """Gets the state of this element.
        
        Only works on:
         - GO.TSWITCH
         - GO.TINPUTBOX
        
        Returns
        -------
        bool
            Whether the switch is on or not 
        """
        if self.type == GO.TSWITCH:
            return self.sprite.get()
        elif self.type == GO.TINPUTBOX:
            return self.sprite.text
        else:
            raise NotImplementedError(
                f'Set text has not been implemented for this element with type {self.name}!'
            )
    
    def __eq__(self, other):
        return self.uid == other

class Graphic:
    def __init__(self, bgcol=GO.CWHITE, TB=True, win=None):
        """The class for making really cool graphic screens :)

        Parameters
        ----------
        bgcol : tuple[int, int, int]
            The colour of the button. For ease of use default colours are provided as GO.C___ (e.g. GO.CGREEN)
        TB : bool, optional
            Whether or not you want the little terminal bar at the bottom, by default True
        win : pygame.Surface, optional
            IF YOU DO NOT SPECIFY: inits pygame, makes a window, does everything
            IF YOU SPECIFY A SURFACE: will NOT init pygame and instead of printing to the screen it prints to the surface
        """
        if win == None:
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
        self.bgcol = bgcol
        self.clock = pygame.time.Clock()
        self.customs = []
        self.statics = []
        self.buttons = []
        self.input_boxes = []
        self.cps = []
        self.toasts = []
        self.store = {}
        self.rel = False
        self.ab = False
        self.touchingbtns = []
        self.pause = False
        self.sprites = pygame.sprite.LayeredDirty()
        self.nextuid = 0
        self.uids = []
        self.scrollsables = []
        self.callbacks = {}
        # This next bit is so users can store their own data and not have it interfere with anything
        class Container: pass
        self.Container = Container()
    def set_caption(caption=None, iconsur=None):
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
    
    def render(self, func=None):
        """You probably don't want to use this unless you really know what it is you are doing."""
        s = pygame.Surface(self.size)
        s.fill((255, 255, 255))
        if func != None: func(GO.ELOADUI)
        for i in self.statics:
            s.blit(i[0], i[1])
        return s
    
    def Loading(self, func): # Function decorator, not to be called
        def func2():
            return Loading(func)(self.WIN, GO.FTITLE)
        return func2
    
    def PBLoading(self, tasks, loadingtxt='Loading{3} {2}% ({0} / {1})'): # TODO: allow aborting
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
        list
            The output list of all the return values of each of the functions inputted
        """
        self.WIN.fill(GO.CWHITE)
        pygame.display.update()
        self.Container.pbar = Progressbar(600, 50)
        res = self.Container.pbar(self.WIN, (self.size[0] - 600) // 2, (self.size[1] - 50) // 2, 5, tasks, loadingtxt)
        asyncio.get_event_loop().stop()
        return res
    
    def CGraphic(self, funcy): # Function decorator, not to be called
        def func2(slf, *args, **kwargs):
            self.Graphic(funcy, slf)(*args, **kwargs) # Yes I know I'm calling it here. Deal with it.
        return func2
    
    def Graphic(self, funcy, slf=None, generator=False, update=True, events=pygame.event.get, mousepos=pygame.mouse.get_pos): # Function decorator, not to be called unless you know what you're doing
        def func2(*args, **kwargs):
            def func(event, element=None, aborted=False):
                if event == GO.EELEMENTCLICK and element.uid in self.callbacks:
                    self.callbacks[element.uid](element)
                if slf == None:
                    return funcy(event, *args, element=element, aborted=aborted, **kwargs)
                else:
                    return funcy(slf, event, *args, element=element, aborted=aborted, **kwargs)
            func(GO.EFIRST)
            prevs = [self.statics.copy(), self.buttons.copy()]
            self.run = True
            self.ab = False
            self.touchingbtns = []
            s = self.render(func)
            while self.run and not self.ab:
                evnts = events()
                if prevs != [self.statics, self.buttons] or self.rel:
                    self.rel = False
                    s = self.render(func)
                    prevs = [self.statics.copy(), self.buttons.copy()]
                self.WIN.fill(self.bgcol)
                self.WIN.blit(s, (0, 0))
                self.touchingbtns = []
                for btn in self.buttons:
                    r, sur = Button(*btn[0])
                    sze = btn[1]
                    r.move_ip(*sze)
                    if not self.pause:
                        col = r.collidepoint(mousepos())
                        if btn[0][-1] != -1 and col:
                            r = pygame.Rect(-btn[0][-1], -btn[0][-1], sur.get_width() + 20 + btn[0][-1]*2, sur.get_height() + 20 + btn[0][-1]*2)
                            r.move_ip(*sze)
                    else: col = False
                    pygame.draw.rect(self.WIN, btn[0][1], r, border_radius=8)
                    self.WIN.blit(sur, (sze[0]+10, sze[1]+10))
                    if col: self.touchingbtns.append((btn, r, sur, sze))
                for btn, r, sur, sze in self.touchingbtns: # repeat so the buttons you are touching appear on top
                    pygame.draw.rect(self.WIN, btn[0][1], r, border_radius=8)
                    self.WIN.blit(sur, (sze[0]+10, sze[1]+10))
                self.TB.update()
                for ibox in self.input_boxes:
                    ibox.draw(self.WIN)
                for i in self.cps:
                    if not self.pause:
                        i.update(mousepos)
                    i.draw()
                self.sprites.update()
                rects = self.sprites.draw(self.WIN)
                pygame.display.update(rects)
                for cls, pass_events in self.customs:
                    if pass_events: cls.execute(self.WIN, evnts)
                    else: cls.execute(self.WIN)
                if func(GO.ETICK) == False:
                    self.run = False
                dels = []
                for i in self.toasts:
                    if i.update(self.WIN) == False:
                        dels.append(i)
                for i in dels: self.toasts.remove(i)
                evs = []
                for event in evnts:
                    evs.append(event)
                    blocked = False
                    if event.type == pygame.QUIT:
                        self.run = False
                    if not self.pause:
                        for ibox in self.input_boxes:
                            if ibox.handle_event(event, pygame.K_RETURN) == False:
                                func(GO.EELEMENTCLICK, Element(GO.TINPUTBOX, self.uids.index(ibox), self, sprite=ibox, txt=str(ibox.get())))
                                blocked = True
                    else:
                        for ibox in self.input_boxes: ibox.active = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.run = False
                        elif self.TB.active != -1:
                            self.TB.pressed(event)
                            blocked = True
                        if event.key == pygame.K_RETURN and self.TB.active == -1 and not any([i.active for i in self.input_boxes]):
                            for sprite in self.sprites:
                                if isinstance(sprite, TextBoxFrame):
                                    if sprite.words:
                                        sprite.reset()
                                    else:
                                        func(GO.EELEMENTCLICK, Element(GO.TTEXTBOX, self.uids.index(sprite), self, sprite=sprite))
                            if not any([isinstance(i, TextBoxFrame) for i in self.sprites]):
                                self.pause = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and not self.pause:
                        if event.button == pygame.BUTTON_LEFT:
                            for i in self.sprites:
                                try:
                                    assert i.isswitch
                                    if i.rect.collidepoint(*mousepos()):
                                        i.state = not i.state
                                        func(GO.EELEMENTCLICK, Element(GO.TSWITCH, self.uids.index(i[0]), self, sw=i))
                                except: pass
                            self.TB.toggleactive(not self.TB.collides(*mousepos()))
                            for i in self.touchingbtns:
                                r = func(GO.EELEMENTCLICK, Element(GO.TBUTTON, self.uids.index(i[0]), self, btn=i))
                                if r != None:
                                    self.run = False
                                    yield [r]
                    elif event.type == pygame.MOUSEWHEEL and not self.pause:
                        for i in self.scrollsables: i.update(event)
                    if not self.pause and not blocked: func(GO.EEVENT, event)
                for i in self.scrollsables:
                    r = i(evs)
                    if isinstance(r, list):
                        if r[0]: self.Abort()
                        else: self.run = False
                yield None
                if update:
                    pygame.display.flip()
                    self.clock.tick(60)
            ret = func(GO.ELAST, aborted=self.ab)
            self.ab = False
            self.run = True
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
        font : pygame.Font, optional
            The font of the text, by default GO.FFONT (other fonts provided as GO.F___)
        col : tuple[int, int, int], optional
            The colour of the toast, by default GO.CACTIVE (other colours provided as GO.C_____)
        txtcol : tuple[int, int, int], optional
            The colour of the text, by default GO.CWHITE
        """
        
        txt = font.render(text, 2, txtcol)
        sur = pygame.Surface((txt.get_size()[0]+spacing*2, txt.get_size()[1]+spacing*2))
        sur.fill([255, 255, 255, 0])
        pygame.draw.rect(sur, col, sur.get_rect(), border_radius=spacing)
        sur.blit(txt, (spacing, spacing))

        pos = GO.PNEW(*GO.PSTACKS[pos])
        npos = self.pos_store(GO.PSTACKS[pos][1](self.size, sur.get_size()), sur.get_size(), pos)
        self.toasts.append(Toast(sur, (npos[0]+GO.PSTACKS[pos][0][0]*dist, npos[1]+GO.PSTACKS[pos][0][1]*dist), npos, timeout))

    def Dropdown(self, elements, spacing=5, font=GO.FFONT, activecol=GO.CACTIVE, bgcol=GO.CBLACK, txtcol=GO.CWHITE, pos=None):
        """Spawns a dropdown!
        This will pause everything else! You will need to click out of the dropdown to exit it.

        Parameters
        ----------
        elements : list
            The choices that you can select
        spacing : int, optional
            The spacing between each element, by default 5
        font : pygame.Font, optional
            The font of the text. For ease of use default fonts are provided as GO.F___ (e.g. GO.FCODEFONT), by default GO.FFONT
        activecol : tuple[int, int, int], optional
            The colour when you hover your mouse over an option, by default GO.CACTIVE
        bgcol : tuple[int, int, int], optional
            The colour of the background of the dropdown, by default GO.CBLACK
        txtcol : tuple[int, int, int], optional
            The colour of the text of the dropdown, by default GO.CWHITE
        pos : tuple[int, int], optional
            The position of the dropdown, by default the mouse location
        For ease of use default colours are provided as GO.C___ (e.g. GO.CGREEN)

        Returns
        -------
        int/None/False
            The index of the input elements list that was selected, else None if nothing selected
            False if you exited from the menu using escape or closing the window. This will also exit the GUI.
        """
        d = dropdown(self.WIN, elements, spacing, font, bgcol, txtcol, activecol, pos)
        if d is False: self.run = False
        return d
    
    def add_custom(self, sprite, pass_events=False):
        """
        Adds a custom sprite to the screen!

        Parameters
        ----------
        sprite : Any
            The sprite to add!
        pass_events : bool
            Whether or not to pass the list of pygame events that have occured that tick to the function
        
        The sprite MUST have the following attribute:
        if pass_events == True:
            `sprite.execute(pygame.Surface, list[pygame.event.Event])` which will be ran every tick, being passed the pygame window which can be blit'ed onto and all the pygame events that have happened that tick
        else:
            `sprite.execute(pygame.Surface)` which will be ran every tick, being passed the pygame window which can be blit'ed onto
        """
        self.customs.append((sprite, pass_events))
    
    def add_text(self, txt, colour, position, font=GO.FFONT):
        """Adds text to the GUI!

        Parameters
        ----------
        txt : str
            The text that will be added to the GUI.
        colour : tuple[int, int, int]
            The colour of the button. For ease of use default colours are provided as GO.C___ (e.g. GO.CGREEN)
        position : GO.P___ (e.g. GO.PRBOTTOM)
            The position on the screen this element will be placed
        font : pygame.Font, optional
            The font of the text. For ease of use default fonts are provided as GO.F___ (e.g. GO.FCODEFONT), by default GO.FFONT
        """
        obj = font.render(txt, 2, colour)
        pos = self.pos_store(GO.PSTACKS[position][1](self.size, obj.get_size()), obj.get_size(), position)
        self.statics.append((obj, pos))
    
    def add_surface(self, obj, position):
        """Adds a surface to the GUI!

        Parameters
        ----------
        obj : pygame.Surface
            The surface to add to the screen!
        position : GO.P___ (e.g. GO.PRBOTTOM)
            The position on the screen this element will be placed
        """
        pos = self.pos_store(GO.PSTACKS[position][1](self.size, obj.get_size()), obj.get_size(), position)
        self.statics.append((obj, pos))
    
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
        """
        self.pos_store(GO.PSTACKS[position][1](self.size, (wid, hei)), (wid, hei), position)
    
    def add_button(self, txt, col, position, txtcol=GO.CBLACK, font=GO.FFONT, on_hover_enlarge=True, callback=None):
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
        font : pygame.Font, optional
            The font of the text. For ease of use default fonts are provided as GO.F___ (e.g. GO.FCODEFONT), by default GO.FFONT
        on_hover_enlarge : bool/int, optional
            Whether to enlarge the button on hover. If this is an int it will be used as the size increase of said button. By default True
        callback : function(Element), optional
            The function to call when this element is pressed, by default None
            Please note that the main function will ALSO be called when this is pressed

        Returns
        -------
        int
            The UID of the created element
        """
        btnconstruct = (txt, col, txtcol, 900, font, (-1 if on_hover_enlarge==False else (10 if on_hover_enlarge==True else on_hover_enlarge)))
        r, _ = Button(*btnconstruct)
        sze = self.pos_store(GO.PSTACKS[position][1](self.size, r.size), r.size, position)
        self.buttons.append((btnconstruct, sze))
        self.uids.append((btnconstruct, sze))
        if callback != None: self.callbacks[len(self.uids) - 1] = callback
        return len(self.uids) - 1
    
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
        int
            the UID of this element
        """
        dialog_box = TextBoxFrame(
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
        pos = self.pos_store(GO.PSTACKS[position][1](self.size, dialog_box.rect.size), dialog_box.rect.size, position)
        dialog_box.rect.topleft = pos
        self.sprites.add(dialog_box)
        self.pause = True
        self.uids.append(dialog_box)
        if callback != None: self.callbacks[len(self.uids) - 1] = callback
        return len(self.uids) - 1
    
    def add_input(self, position, font=GO.FSMALL, width=None, resize=GO.RHEIGHT, placeholder='Type Here', maximum=100, start='', callback=None):
        """Adds an input box :)

        Parameters
        ----------
        position : GO.P___ (e.g. GO.PRBOTTOM)
            The position on the screen this element will be placed
        font : pygame.Font, optional
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
        int
            the UID of this element
        """
        sze = list(font.size(placeholder))
        if maximum == None: maximum = sze+5
        if width != None: sze[0] = width+5
        else: sze[0] += 5
        sze[1] += 10
        pos = self.pos_store(GO.PSTACKS[position][1](self.size, sze), sze, position)
        ibox = InputBox(*pos, *sze, resize, placeholder, font, maximum, start) # TODO: Positioning and custom width & height & resize
        self.input_boxes.append(ibox)
        self.uids.append(ibox)
        if callback != None: self.callbacks[len(self.uids) - 1] = callback
        return len(self.uids) - 1
    
    def add_num_input(self, position, font=GO.FSMALL, width=None, resize=GO.RHEIGHT, start=0, bounds=(float('-inf'), float('inf')), callback=None):
        """Adds an input box for numbers :)

        Parameters
        ----------
        position : GO.P___ (e.g. GO.PRBOTTOM)
            The position on the screen this element will be placed
        font : pygame.Font, optional
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
        int
            the UID of this element
        """
        sze = list(font.size(str(start)))
        if width != None: sze[0] = font.size('9'*width)[0]+5
        sze[0] += 5
        sze[1] += 10
        pos = self.pos_store(GO.PSTACKS[position][1](self.size, sze), sze, position)
        ibox = NumInputBox(*pos, *sze, resize, start, *bounds, font) # TODO: Positioning and custom width & height & resize
        self.input_boxes.append(ibox)
        self.uids.append(ibox)
        if callback != None: self.callbacks[len(self.uids) - 1] = callback
        return len(self.uids) - 1
    
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
        int
            the UID of this element
        """
        sze = (size*1.5, size*1.5)
        pos = self.pos_store(GO.PSTACKS[position][1](self.size, sze), sze, position)
        sw = Switch(self.WIN, pos[0]+size/4, pos[1]+size/4, size, 2, default)
        self.sprites.add(sw)
        self.uids.append(sw)
        if callback != None: self.callbacks[len(self.uids) - 1] = callback
        return len(self.uids) - 1

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
        int
            the UID of this element
        """
        pos = self.pos_store(GO.PSTACKS[position][1](self.size, (size, size)), (size, size), position)
        btn = ColourPickerBTN(self.WIN, *pos, size, sow)
        self.cps.append(btn)
        self.uids.append(btn)
        return len(self.uids) - 1
    
    def add_Scrollable(self, position, size, sos, outline=10, bar=True):
        """Adds a Scrollable window to the Graphic screen!
        This is like another really tiny Graphic screen inside the big one, but the tiny one you can scroll!

        Parameters
        ----------
        position : GO.P___ (e.g. GO.PRBOTTOM)
            The position on the screen this element will be placed
        size : tuple[int, int]
            The size of the scrollable box
        sos : tuple[int, int]
            The size of the screen (How big the created tiny Graphic screen will be)
        outline : int, optional
            The thickness of the outline, 0 to turn it off, by default 10
        bar : bool, optional
            Whether or not to have a little red scrollbar in the side, by default True
            The thickness of the scrollbar is constant (10)

        Returns
        -------
        tuple[int, Graphic]
            (the UID of the element, The Graphic class created which is put onto the main one)
        """
        pos = self.pos_store(GO.PSTACKS[position][1](self.size, size), size, position)
        s = GScrollable(self.WIN, pos, size, sos, outline, bar)
        self.scrollsables.append(s)
        self.uids.append(s)
        return (len(self.uids) - 1, s.G)
    
    def pos_store(self, pos, sze, func):
        sizeing = GO.PSTACKS[func][0]
        if func not in self.store:
            self.store[func] = [sze[0]*sizeing[0], sze[1]*sizeing[1]]
            return pos
        pos2 = [None, None]
        if pos[0] < 0: pos2[0] = pos[0]+(0-self.store[func][0])*sizeing[0]
        else: pos2[0] = pos[0]+self.store[func][0]
        if pos[1] < 0: pos2[1] = pos[1]+(0-self.store[func][1])*sizeing[1]
        else: pos2[1] = pos[1]+self.store[func][1]
        self.store[func] = [self.store[func][0] + sze[0]*sizeing[0], self.store[func][1] + sze[1]*sizeing[1]]
        return pos2
    
    def Reload(self):
        self.rel = True
    
    def Clear(self):
        GO.PIDX = 0
        self.statics = []
        self.customs = []
        self.buttons = []
        self.input_boxes = []
        self.store = {}
        self.sprites.empty()
        self.pause = False
        self.nextuid = 0
        self.uids = []
        self.scrollsables = []
        self.cps = []
        self.callbacks = {}
    
    def Abort(self):
        self.ab = True
