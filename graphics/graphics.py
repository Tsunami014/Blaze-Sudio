import pygame
pygame.init()
try:
    import graphics.graphics_options as GO
    from graphics.loading import Loading
    from graphics.GUI import TextBoxFrame, InputBox, Button, Switch, dropdown, NumInputBox, Scrollable, ColourPickerBTN
    from graphics.GUI.textboxify.borders import LIGHT
except:
    import graphics_options as GO
    from loading import Loading
    from GUI import TextBoxFrame, InputBox, Button, Switch, dropdown, NumInputBox, Scrollable, ColourPickerBTN
    from GUI.textboxify.borders import LIGHT

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
        
        Returns
        -------
        bool
            Whether the switch is on or not 
        """
        if self.type == GO.TSWITCH:
            return self.sprite.get()
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
        self.statics = []
        self.buttons = []
        self.input_boxes = []
        self.cps = []
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
                self.run = func(GO.ETICK)
                evs = []
                for event in events():
                    evs.append(event)
                    blocked = False
                    if event.type == pygame.QUIT:
                        self.run = False
                    for ibox in self.input_boxes:
                        if ibox.handle_event(event, pygame.K_RETURN) == False:
                            func(GO.EELEMENTCLICK, Element(GO.TINPUTBOX, self.uids.index(ibox), self, sprite=ibox, txt=str(ibox.get())))
                            blocked = True
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
                                func(GO.EELEMENTCLICK, Element(GO.TBUTTON, self.uids.index(i[0]), self, btn=i))
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
            yield [ret]
        def func3(*args, **kwargs):
            f = func2(*args, **kwargs)
            while True:
                y = next(f)
                if y != None:
                    return y[0]
        if generator: return func2
        else: return func3

    def Dropdown(self, elements, spacing=5, font=GO.FFONT, activecol=GO.CACTIVE, bgcol=GO.CBLACK, txtcol=GO.CWHITE):
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
        For ease of use default colours are provided as GO.C___ (e.g. GO.CGREEN)

        Returns
        -------
        int/None/False
            The index of the input elements list that was selected, else None if nothing selected
            False if you exited from the menu using escape or closing the window. This will also exit the GUI.
        """
        d = dropdown(self.WIN, elements, spacing, font, bgcol, txtcol, activecol)
        if d is False: self.run = False
        return d
    
    
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

if __name__ == '__main__':
    from time import sleep
    t = input('Please input the starting text for the middle: ')
    G = Graphic()
    @G.Loading
    def test_loading(self):
        for self.i in range(10):
            sleep(1)
    
    @G.Graphic
    def test(event, txt, element=None, aborted=False): # You do not need args and kwargs if you KNOW that your function will not take them in. Include what you need.
        if event == GO.EFIRST: # First, before anything else happens in the function
            G.Container.txt = txt
        if event == GO.ELOADUI: # Load the graphics
            CTOP = GO.PNEW([1, 0], GO.PSTACKS[GO.PCTOP][1]) # Bcos usually the Center Top makes the elements stack down, so I make a new thing that stacks sideways
            LBOT = GO.PNEW([0, -1], GO.PSTACKS[GO.PLBOTTOM][1])
            try:
                prevs = [G.uids[i].get() for i in (G.Container.switches+[G.Container.numinp,G.Container.inp])] + [G.uids[G.Container.colour].picker.p]
                prevTG = [G.uids[G.Container.scrollable].G.uids[G.Container.otherswitch].get(), G.uids[G.Container.scrollable].scroll]
            except:
                prevs = [False, False, 0, '', (0, 0.5)]
                prevTG = [False, 0]
            G.Clear()
            G.add_text('HI', GO.CGREEN, GO.PRBOTTOM, GO.FTITLE)
            G.add_text(':) ', GO.CBLACK, GO.PRBOTTOM, GO.FTITLE)
            G.add_empty_space(GO.PCCENTER, 0, -150) # Yes, you can have negative space. This makes the next things shifted the other direction.
            G.add_text('This is a cool thing', GO.CBLUE, GO.PCCENTER)
            G.add_text('Sorry, I meant a cool TEST', GO.CRED, GO.PCCENTER)
            G.add_text(G.Container.txt, GO.CGREEN, GO.PCCENTER)
            G.add_empty_space(LBOT, 0, 20)
            G.add_button('Button 1 :D', GO.CYELLOW, LBOT)
            G.add_text('Buttons above [^] and below [v]', GO.CBLUE, LBOT)
            G.add_button('Textbox test', GO.CBLUE, LBOT)
            G.add_button('Loading test', GO.CGREEN, LBOT)
            G.Container.exitbtn = G.add_button('EXIT', GO.CRED, GO.PLCENTER)
            G.add_empty_space(CTOP, -150, 0) # Center it a little more
            G.add_text('Are you ', GO.CBLACK, CTOP)
            G.add_text('happy? ', GO.CGREEN, CTOP)
            G.add_text('Or sad?', GO.CRED, CTOP)
            G.Container.inp = G.add_input(GO.PCCENTER, GO.FFONT, maximum=16, start=prevs[3])
            G.add_empty_space(GO.PCCENTER, 0, 50)
            G.Container.numinp = G.add_num_input(GO.PCCENTER, GO.FFONT, 4, start=prevs[2], bounds=(-255, 255))
            G.Container.switches = [
                G.add_switch(GO.PRTOP, 40, prevs[0]),
                G.add_switch(GO.PRTOP, default=prevs[1])
            ]
            G.Container.colour = G.add_colour_pick(GO.PRTOP)
            G.uids[G.Container.colour].picker.p = prevs[4]
            TOPLEFT = GO.PSTATIC(10, 10) # Set a custom coordinate that never changes
            G.Container.scrollable, S = G.add_Scrollable(TOPLEFT, (250, 200), (250, 350))
            G.uids[G.Container.scrollable].scroll = prevTG[1]
            S.add_empty_space(GO.PCTOP, 10, 20)
            S.add_button('Scroll me!', GO.CBLUE, GO.PCTOP)
            G.Container.otherinp = S.add_input(GO.PCTOP, placeholder='I reset!!')
            S.add_button('Bye!', GO.CGREEN, GO.PCTOP)
            def pressed(elm):
                G.Container.txt = 'You pressed the button in the Scrollable :)'
                G.Reload()
            S.add_button('Press me!', GO.CRED, GO.PCTOP, callback=pressed)
            G.Container.otherswitch = S.add_switch(GO.PCTOP, default=prevTG[0])
        elif event == GO.ETICK: # This runs every 1/60 secs (each tick)
            return True # Return whether or not the loop should continue.
        elif event == GO.EELEMENTCLICK: # Some UI element got clicked!
            if element.type == GO.TBUTTON:
                # This gets passed 'element': the element that got clicked. TODO: make an Element class
                # The == means element's uid == __
                # UID gets generated based off order: so UID of 2 means second thing created that makes a UID.
                # When you create a thing that makes a UID it returns it. e.g. button1 = G.add_button(etc.)
                # So in that example button1 is the UID. Maybe try saving it to the container tho! Example shown by the exit button.
                if element == 2:
                    succeeded, ret = test_loading()
                    G.Container.txt = ('Ran for %i seconds%s' % (ret['i']+1, (' Successfully! :)' if succeeded else ' And failed :(')))
                    G.Reload()
                elif element == G.Container.exitbtn:
                    G.Abort()
                elif element == 1:
                    bot = GO.PNEW([0, 0], GO.PSTACKS[GO.PCBOTTOM][1], 1)
                    G.add_TextBox('HALLOOOO! :)', bot)
                    G.Container.idx = 0
                else:
                    G.Container.txt = element.txt # put name of button in middle
                    G.Reload()
            elif element.type == GO.TTEXTBOX:
                if G.Container.idx == 0:
                    element.set_text("Happy coding!")
                    G.Container.idx = 1
                else:
                    element.remove()
            elif element.type == GO.TINPUTBOX:
                G.Container.txt = element.txt
                element.remove()
                G.Reload()
        elif event == GO.EEVENT: # When something like a button is pressed. Is passed 'element' too, but this time it is an event
            if element.type == pygame.KEYDOWN:
                if element.key == pygame.K_s and element.mod & pygame.KMOD_CTRL:
                    G.Container.txt = 'Saved! (Don\'t worry - this does nothing)'
                    G.Reload()
            elif element.type == pygame.MOUSEBUTTONDOWN and element.button == pygame.BUTTON_RIGHT:
                opts = ['HI', 'BYE', 'HI AGAIN']
                resp = G.Dropdown(opts)
                if isinstance(resp, int):
                    G.Container.txt = opts[resp]
                    G.Reload()
        elif event == GO.ELAST:
            # This also gets passed 'aborted': Whether you aborted or exited the screen
            return {
                'Aborted?': aborted, 
                'Text in textbox': G.uids[G.Container.inp].get(),
                'Num in num textbox': G.uids[G.Container.numinp].get(),
                'Big switch state': G.uids[G.Container.switches[0]].get(),
                'Small switch state': G.uids[G.Container.switches[1]].get(),
                'Switch in scrollable area state': G.uids[G.Container.scrollable].G.uids[G.Container.otherswitch].get(),
                'Text in textbox in scrollable area': G.uids[G.Container.scrollable].G.uids[G.Container.otherinp].get()
                } # Whatever you return here will be returned by the function
    
    print(test('Right click! ' + t))
    
    # Copy this scaffold for your own code :)
    # Args and kwargs are passed through from the initial call of the func
    @G.Graphic # If you use classes, make this CGraphics and add a `self` argument to the function
    def funcname(event, *args, element=None, aborted=False, **kwargs):
        if event == GO.EFIRST:
            pass
        elif event == GO.ELOADUI:
            G.Clear()
        elif event == GO.ETICK:
            return True # Return whether or not the loop should continue.
        elif event == GO.EELEMENTCLICK: # Passed 'element'
            pass
        elif event == GO.EEVENT: # Passed 'element' (but is event)
            pass
        elif event == GO.ELAST: # Passed 'aborted'
            pass # Whatever you return here will be returned by the function
    pygame.quit() # this here for very fast quitting
