import pygame
pygame.init()
try:
    import graphics.graphics_options as GO
    from graphics.GUI.randomGUIelements import Button
except:
    import graphics_options as GO
    from GUI.randomGUIelements import Button

class Graphic:
    def __init__(self):
        self.WIN = pygame.display.set_mode()
        self.clock = pygame.time.Clock()
        self.statics = []
        self.buttons = []
        self.store = {}
    def set_caption(caption):
        pygame.display.set_caption(caption)
    
    def render(self, func=None):
        s = pygame.Surface(self.WIN.get_size())
        s.fill((255, 255, 255))
        if func != None: func(True)
        for i in self.statics:
            s.blit(i[0], i[1])
        return s
    
    def graphic(self, func):
        def func2():
            prevs = [self.statics.copy(), self.buttons.copy()]
            run = True
            s = self.render(func)
            while run:
                if prevs != [self.statics, self.buttons]:
                    s = self.render(func)
                    prevs = [self.statics.copy(), self.buttons.copy()]
                self.WIN.fill((255, 255, 255))
                self.WIN.blit(s, (0, 0))
                touchingbtns = []
                st = self.store.copy()
                for btn in self.buttons:
                    r, sur = Button(*btn[0])
                    sze = self.pos_store(GO.PSTACKS[btn[1]][1](self.WIN.get_size(), r.size), r.size, btn[1])
                    r.move_ip(*sze)
                    col = r.collidepoint(pygame.mouse.get_pos())
                    if btn[0][-1] != -1 and col:
                        r = pygame.Rect(-btn[0][-1], -btn[0][-1], sur.get_width() + 20 + btn[0][-1]*2, sur.get_height() + 20 + btn[0][-1]*2)
                        r.move_ip(*sze)
                    pygame.draw.rect(self.WIN, btn[0][1], r, border_radius=8)
                    self.WIN.blit(sur, (sze[0]+10, sze[1]+10))
                    if col: touchingbtns.append((btn, r, sur, sze))
                self.store = st.copy()
                for btn, r, sur, sze in touchingbtns: # repeat so the buttons you are touching appear on top
                    pygame.draw.rect(self.WIN, btn[0][1], r, border_radius=8)
                    self.WIN.blit(sur, (sze[0]+10, sze[1]+10))
                self.store = st
                run = func(False)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                            return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == pygame.BUTTON_LEFT:
                            for i in touchingbtns:
                                func(i)
                pygame.display.flip()
                self.clock.tick(60)
        return func2
    
    def add_text(self, txt, colour, position, font=GO.FFONT):
        obj = font.render(txt, 2, colour)
        pos = self.pos_store(GO.PSTACKS[position][1](self.WIN.get_size(), obj.get_size()), obj.get_size(), position)
        self.statics.append((obj, pos))
    
    def add_empty_space(self, position, wid, hei):
        empty = (255,255,255,0) 
        obj = pygame.Surface((wid, hei))
        obj.fill(empty)
        pos = self.pos_store(GO.PSTACKS[position][1](self.WIN.get_size(), obj.get_size()), obj.get_size(), position)
        self.statics.append((obj, pos))
    
    def add_button(self, txt, col, position, txtcol=GO.CBLACK, font=GO.FFONT, on_hover_enlarge=True):
        self.buttons.append(((txt, col, txtcol, 900, font, (-1 if on_hover_enlarge==False else (10 if on_hover_enlarge==True else on_hover_enlarge))), position))
    
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
    
    def clear(self):
        self.statics = []
        self.buttons = []
        self.store = {}

if __name__ == '__main__':
    G = Graphic()
    @G.graphic
    def test(ui):
        if ui == True: # Load the graphics
            G.clear()
            G.add_text('HI', GO.CGREEN, GO.PRBOTTOM, GO.FTITLE)
            G.add_text(':) ', GO.CBLACK, GO.PRBOTTOM, GO.FTITLE)
            G.add_text('This is a cool thing', GO.CBLUE, GO.PCCENTER)
            G.add_text('Sorry, I meant a cool TEST', GO.CRED, GO.PCCENTER)
            G.add_empty_space(GO.PCBOTTOM, 10, 20)
            G.add_button('Button 1 :D', GO.CYELLOW, GO.PCBOTTOM)
            G.add_button('Button 2 :(  hi', GO.CBLUE, GO.PCBOTTOM)
            G.add_text('Are you ', GO.CBLACK, GO.PLTOP)
            G.add_text('happy? ', GO.CGREEN, GO.PLTOP)
            G.add_text('Or sad?', GO.CRED, GO.PLTOP)
        elif ui == False: # This runs every 1/60 secs
            pass
        else: # Some UI element got clicked!
            print(ui)
        return True
    test()
    pygame.quit() # this here for very fast quitting
