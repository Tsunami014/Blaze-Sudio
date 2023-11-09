import pygame
pygame.init()
try:
    import graphics.graphics_options as GO
    from graphics.loading import Loading
    from graphics.GUI.randomGUIelements import Button
except:
    import graphics_options as GO
    from loading import Loading
    from GUI.randomGUIelements import Button

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

class Graphic:
    def __init__(self):
        self.WIN = pygame.display.set_mode()
        pygame.display.toggle_fullscreen()
        self.TB = TerminalBar(self.WIN)
        self.size = (self.WIN.get_width(), self.WIN.get_height()-26)
        self.clock = pygame.time.Clock()
        self.statics = []
        self.buttons = []
        self.store = {}
        self.rel = False
        # This next bit is so users can store their own data and not have it interfere with anything
        class Container: pass
        self.container = Container()
    def set_caption(caption):
        pygame.display.set_caption(caption)
    
    def render(self, func=None):
        s = pygame.Surface(self.size)
        s.fill((255, 255, 255))
        if func != None: func(GO.TLOADUI)
        for i in self.statics:
            s.blit(i[0], i[1])
        return s
    
    def Loading(self, func):
        def func2():
            return Loading(func)(self.WIN, GO.FTITLE)
        return func2
    
    def graphic(self, funcy):
        def func2(slf=None):
            def func(*args):
                if slf != None:
                    return funcy(slf, *args)
                else:
                    return funcy(*args)
            func(GO.TFIRST)
            prevs = [self.statics.copy(), self.buttons.copy()]
            run = True
            s = self.render(func)
            while run:
                if prevs != [self.statics, self.buttons] or self.rel:
                    self.rel = False
                    s = self.render(func)
                    prevs = [self.statics.copy(), self.buttons.copy()]
                self.WIN.fill((255, 255, 255))
                self.WIN.blit(s, (0, 0))
                touchingbtns = []
                for btn in self.buttons:
                    r, sur = Button(*btn[0])
                    sze = btn[1]
                    r.move_ip(*sze)
                    col = r.collidepoint(pygame.mouse.get_pos())
                    if btn[0][-1] != -1 and col:
                        r = pygame.Rect(-btn[0][-1], -btn[0][-1], sur.get_width() + 20 + btn[0][-1]*2, sur.get_height() + 20 + btn[0][-1]*2)
                        r.move_ip(*sze)
                    pygame.draw.rect(self.WIN, btn[0][1], r, border_radius=8)
                    self.WIN.blit(sur, (sze[0]+10, sze[1]+10))
                    if col: touchingbtns.append((btn, r, sur, sze))
                for btn, r, sur, sze in touchingbtns: # repeat so the buttons you are touching appear on top
                    pygame.draw.rect(self.WIN, btn[0][1], r, border_radius=8)
                    self.WIN.blit(sur, (sze[0]+10, sze[1]+10))
                run = func(GO.TTICK)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                            return
                        elif self.TB.active != -1:
                            self.TB.pressed(event)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == pygame.BUTTON_LEFT:
                            self.TB.toggleactive(not self.TB.collides(*event.pos))
                            for i in touchingbtns:
                                func(GO.TELEMENTCLICK, i)
                self.TB.update()
                pygame.display.flip()
                self.clock.tick(60)
            return func(GO.TLAST)
        return func2
    
    def add_text(self, txt, colour, position, font=GO.FFONT):
        obj = font.render(txt, 2, colour)
        pos = self.pos_store(GO.PSTACKS[position][1](self.size, obj.get_size()), obj.get_size(), position)
        self.statics.append((obj, pos))
    
    def add_empty_space(self, position, wid, hei):
        self.pos_store(GO.PSTACKS[position][1](self.size, (wid, hei)), (wid, hei), position)
    
    def add_button(self, txt, col, position, txtcol=GO.CBLACK, font=GO.FFONT, on_hover_enlarge=True):
        btnconstruct = (txt, col, txtcol, 900, font, (-1 if on_hover_enlarge==False else (10 if on_hover_enlarge==True else on_hover_enlarge)))
        r, _ = Button(*btnconstruct)
        sze = self.pos_store(GO.PSTACKS[position][1](self.size, r.size), r.size, position)
        self.buttons.append((btnconstruct, sze))
    
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
    
    def reload(self):
        self.rel = True
    
    def clear(self):
        self.statics = []
        self.buttons = []
        self.store = {}

if __name__ == '__main__':
    from time import sleep
    G = Graphic()
    @G.Loading
    def test_loading(self):
        for self.i in range(10):
            sleep(1)
    
    @G.graphic
    def test(event, element=None): # If this was a class you could do `def test(self, event, element=None)` as it can work for that
        if event == GO.TFIRST: # First, before anything else happens in the function
            G.container.txt = 'Try pressing a button!'
        if event == GO.TLOADUI: # Load the graphics
            G.clear()
            G.add_text('HI', GO.CGREEN, GO.PRBOTTOM, GO.FTITLE)
            G.add_text(':) ', GO.CBLACK, GO.PRBOTTOM, GO.FTITLE)
            G.add_empty_space(GO.PCCENTER, 0, -150) # Yes, you can have negative space. This makes the next things shifted the other direction.
            G.add_text('This is a cool thing', GO.CBLUE, GO.PCCENTER)
            G.add_text('Sorry, I meant a cool TEST', GO.CRED, GO.PCCENTER)
            G.add_text(G.container.txt, GO.CGREEN, GO.PCCENTER)
            G.add_empty_space(GO.PCBOTTOM, 0, 20)
            G.add_button('Button 1 :D', GO.CYELLOW, GO.PCBOTTOM)
            G.add_text('Buttons above [^] and below [v]', GO.CBLUE, GO.PCBOTTOM)
            G.add_button('Button 2 :(  hi', GO.CBLUE, GO.PCBOTTOM)
            G.add_button('Loading test', GO.CGREEN, GO.PCBOTTOM)
            G.add_text('Are you ', GO.CBLACK, GO.PLTOP)
            G.add_text('happy? ', GO.CGREEN, GO.PLTOP)
            G.add_text('Or sad?', GO.CRED, GO.PLTOP)
        elif event == GO.TTICK: # This runs every 1/60 secs (each tick)
            return True # Return whether or not the loop should continue.
        elif event == GO.TELEMENTCLICK: # Some UI element got clicked! (currently only buttons, so we know what to do here)
            if element[0][0][0] == 'Loading test':
                succeeded, ret = test_loading()
                G.container.txt = ('Ran for %i seconds%s' % (ret['i']+1, (' Successfully! :)' if succeeded else ' And failed :(')))
            else: G.container.txt = element[0][0][0] # print name of button
            G.reload()
        elif event == GO.TLAST:
            pass # Whatever you return here will be returned by the function
    
    # Copy this scaffold for your own code :)
    @G.graphic
    def funcname(event, element=None):
        if event == GO.TFIRST:
            pass
        elif event == GO.TLOADUI:
            G.clear()
        elif event == GO.TTICK:
            return True # Return whether or not the loop should continue.
        elif event == GO.TELEMENTCLICK:
            pass
        elif event == GO.TLAST:
            pass # Whatever you return here will be returned by the function
    test()
    pygame.quit() # this here for very fast quitting
