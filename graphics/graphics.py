import pygame
pygame.init()
try:
    import graphics.graphics_options as GO
    from graphics.loading import Loading
    from graphics.GUI import TextBoxFrame, InputBox, Button
    from graphics.GUI.textboxify.borders import LIGHT
except:
    import graphics_options as GO
    from loading import Loading
    from GUI import TextBoxFrame, InputBox, Button
    from GUI.textboxify.borders import LIGHT

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

class Element: # Button or TextBoxFrame
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
        except KeyError as e:
            raise TypeError(
                f'{self.name} Element requires kwarg "{str(e)}" but was not provided!'
            )
    
    def remove(self):
        """Removes an element.

        Only works on:
         - GO.TTEXTBOX (A TextBox element)
         - GO.TINPUTBOX
        """
        if self.type == GO.TTEXTBOX:
            self.G.sprites.remove(self.sprite)
        elif self.type == GO.TINPUTBOX:
            self.G.input_boxes.remove(self.sprite)
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
    
    def __eq__(self, other):
        return self.uid == other

class Graphic:
    def __init__(self):
        self.WIN = pygame.display.set_mode()
        pygame.display.toggle_fullscreen()
        self.TB = TerminalBar(self.WIN)
        self.size = (self.WIN.get_width(), self.WIN.get_height()-26)
        self.clock = pygame.time.Clock()
        self.statics = []
        self.buttons = []
        self.input_boxes = []
        self.store = {}
        self.rel = False
        self.ab = False
        self.touchingbtns = []
        self.pause = False
        self.sprites = pygame.sprite.LayeredDirty()
        self.nextuid = 0
        self.uids = []
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
    
    def Graphic(self, funcy, slf=None): # Function decorator, not to be called
        def func2(*args, **kwargs):
            def func(event, element=None, aborted=False):
                if slf == None:
                    return funcy(event, *args, element=element, aborted=aborted, **kwargs)
                else:
                    return funcy(slf, event, *args, element=element, aborted=aborted, **kwargs)
            func(GO.EFIRST)
            prevs = [self.statics.copy(), self.buttons.copy()]
            run = True
            self.ab = False
            self.touchingbtns = []
            s = self.render(func)
            while run and not self.ab:
                if prevs != [self.statics, self.buttons] or self.rel:
                    self.rel = False
                    s = self.render(func)
                    prevs = [self.statics.copy(), self.buttons.copy()]
                self.WIN.fill((255, 255, 255))
                self.WIN.blit(s, (0, 0))
                self.touchingbtns = []
                for btn in self.buttons:
                    r, sur = Button(*btn[0])
                    sze = btn[1]
                    r.move_ip(*sze)
                    if not self.pause:
                        col = r.collidepoint(pygame.mouse.get_pos())
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
                run = func(GO.ETICK)
                for event in pygame.event.get():
                    blocked = False
                    if event.type == pygame.QUIT:
                        run = False
                    for ibox in self.input_boxes:
                        if ibox.handle_event(event, pygame.K_RETURN) == False:
                            func(GO.EELEMENTCLICK, Element(GO.TINPUTBOX, self.uids.index(ibox), self, sprite=ibox, txt=ibox.text))
                            blocked = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
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
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == pygame.BUTTON_LEFT:
                            self.TB.toggleactive(not self.TB.collides(*event.pos))
                            for i in self.touchingbtns:
                                func(GO.EELEMENTCLICK, Element(GO.TBUTTON, self.uids.index(i[0]), self, btn=i))
                    if not self.pause and not blocked: func(GO.EEVENT, event)
                self.TB.update()
                for ibox in self.input_boxes:
                    ibox.draw(self.WIN)
                self.sprites.update()
                rects = self.sprites.draw(self.WIN)
                pygame.display.update(rects)
                pygame.display.flip()
                self.clock.tick(60)
            ret = func(GO.ELAST, aborted=self.ab)
            self.ab = False
            return ret
        return func2
    
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
    
    def add_button(self, txt, col, position, txtcol=GO.CBLACK, font=GO.FFONT, on_hover_enlarge=True):
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
        return len(self.uids) - 1
    
    def add_TextBox(self, txt, position, border=LIGHT, indicator=None, portrait=None):
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
        return len(self.uids) - 1
    
    def add_input(self, position):
        ibox = InputBox(100, 100, 140, 32, 'type here!') # TODO: Positioning and custom width & height & resize
        self.input_boxes.append(ibox)
        self.uids.append(ibox)
        return len(self.uids) - 1
    
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
        self.statics = []
        self.buttons = []
        self.input_boxes = []
        self.store = {}
        self.sprites.empty()
        self.pause = False
        self.nextuid = 0
        self.uids = []
    
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
            CTOP = GO.PNEW([1, 0], GO.PSTACKS[GO.PCTOP][1], 0) # Bcos usually the Center Top makes the elements stack down, so I make a new thing that stacks sideways
            G.Clear()
            G.add_text('HI', GO.CGREEN, GO.PRBOTTOM, GO.FTITLE)
            G.add_text(':) ', GO.CBLACK, GO.PRBOTTOM, GO.FTITLE)
            G.add_empty_space(GO.PCCENTER, 0, -150) # Yes, you can have negative space. This makes the next things shifted the other direction.
            G.add_text('This is a cool thing', GO.CBLUE, GO.PCCENTER)
            G.add_text('Sorry, I meant a cool TEST', GO.CRED, GO.PCCENTER)
            G.add_text(G.Container.txt, GO.CGREEN, GO.PCCENTER)
            G.add_empty_space(GO.PCBOTTOM, 0, 20)
            G.add_button('Button 1 :D', GO.CYELLOW, GO.PCBOTTOM)
            G.add_text('Buttons above [^] and below [v]', GO.CBLUE, GO.PCBOTTOM)
            G.add_button('Textbox test', GO.CBLUE, GO.PCBOTTOM)
            G.add_button('Loading test', GO.CGREEN, GO.PCBOTTOM)
            G.Container.exitbtn = G.add_button('EXIT', GO.CRED, GO.PCBOTTOM)
            G.add_empty_space(CTOP, -150, 0) # Center it a little more
            G.add_text('Are you ', GO.CBLACK, CTOP)
            G.add_text('happy? ', GO.CGREEN, CTOP)
            G.add_text('Or sad?', GO.CRED, CTOP)
            G.add_input(GO.PCCENTER)
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
        elif event == GO.ELAST:
            # This also gets passed 'aborted': Whether you aborted or exited the screen
            return aborted # Whatever you return here will be returned by the function
    
    print(test(t))
    
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
