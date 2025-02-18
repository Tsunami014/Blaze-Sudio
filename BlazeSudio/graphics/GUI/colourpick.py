import pygame
from BlazeSudio.graphics.base import Element, ReturnState
from BlazeSudio.graphics import mouse, options as GO # TODO: Replace more values in here with the GO variants

# Thanks to https://stackoverflow.com/questions/73517832/how-to-make-an-color-picker-in-pygame :)
# Too big to go in another file

class ValuePicker:
    def __init__(self, x, y, w, h, parenth, default=0, type=0, border=False):
        self.size = (w, h)
        self.type = type
        self.border = border
        self.bounds = 360 if type == 0 else 100
        self.rad = h//2
        self.pwidth = w-self.rad*2
        self.rect = pygame.Rect(x, y, w, h)
        self.pos = (x+h//2, y+h//3)
        self.image = pygame.Surface((self.pwidth, self.pwidth))
        self.image.fill((255, 255, 255))
        for i in range(self.pwidth):
            colour = pygame.Color(0)
            hsla = [360, 100, 50, 100]
            hsla[self.type] = int(self.bounds*i/self.pwidth)
            colour.hsla = tuple(hsla)
            pygame.draw.rect(self.image, colour, (i, 0, 1, h-2*h//3))
        try:
            self.p = (1/self.bounds)*default
        except:
            self.p = 0
        self.twod = pygame.Surface((self.pwidth, parenth))
        self.twod.fill((255, 255, 255))
        for i in range(self.pwidth):
            for j in range(parenth):
                try:
                    colour = pygame.Color(0)
                    hsla = [360, 100, 100-int((100/parenth)*j*2*(100/parenth)), 100]
                    hsla[self.type] = 0
                    colour.hsla = tuple(hsla)
                    pygame.draw.rect(self.twod, colour, (i, j, 1, 1))
                except:
                    pass
        self.p = (max(0, min(self.p, 1)))
    
    def set_position(self, x, y):
        h = self.size[1]
        self.rect = pygame.Rect(x, y, *self.size)
        self.pos = (x+h//2, y+h//3)
    
    def get_twod(self, w, h):
        s = self.twod.copy()
        s.set_alpha(300-300*self.p)
        return pygame.transform.scale(s, (w, h))

    def get_colour(self):
        colour = pygame.Color(0)
        hsla = [360, 100, 50, 100]
        hsla[self.type] = int(self.bounds * self.p)
        colour.hsla = tuple(hsla)
        return colour

    def update(self, mousePos):
        if self.rect.collidepoint(mousePos):
            mouse.Mouse.set(mouse.MouseState.PICK)
            if pygame.mouse.get_pressed()[0]:
                self.p = (mousePos[0] - self.rect.left - self.rad) / self.pwidth
                self.p = max(0, min(self.p, 1))
                return True
        return False

    def draw(self, surf):
        if not self.border:
            pygame.draw.rect(surf, (255, 255, 255), self.rect)
        else:
            pygame.draw.rect(surf, (255, 255, 255), self.rect, border_radius=8, border_top_left_radius=0, border_top_right_radius=0)
        surf.blit(self.image, self.pos)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pygame.draw.circle(surf, self.get_colour(), center, self.rect.height // 2)

class ColourPicker:
    def __init__(self, x, y, border=5, values=[1], w=100, h=None):
        self.pwidth = w
        self.pheight = h or w
        self.values = [ValuePicker(x-border, y+self.pheight+border+i*50, w+border*2, 50, self.pheight, [0, 100, 50, 100][values[i]], values[i], i==len(values)-1) for i in range(len(values))]
        self.rect = pygame.Rect(x-border, y-border, self.pwidth+border*2, self.pheight+border*2)
        self.imrect = pygame.Rect(x, y, self.pwidth, self.pheight)
        self.border = border
        self.image = pygame.Surface((self.pwidth, self.pheight))
        self.image.fill((255, 255, 255))
        for i in range(self.pwidth):
            for j in range(self.pheight):
                try:
                    colour = pygame.Color(0)
                    colour.hsla = (int((360/self.pwidth)*i/2*(360/self.pwidth)), 100, 100-int((100/self.pheight)*j*2*(100/self.pheight)), 100)
                    pygame.draw.rect(self.image, colour, (i, j, 1, 1))
                except:
                    pass
        self.p = (0, 0)
    
    def set_position(self, x, y):
        
        for i in range(len(self.values)):
            self.values[i].set_position(x-self.border, y+self.pheight+self.border+i*50)
        
        self.rect = pygame.Rect(x-self.border, y-self.border, self.pwidth+self.border*2, self.pheight+self.border*2)
        self.imrect = pygame.Rect(x, y, self.pwidth, self.pheight)
    
    def get_size(self):
        sizes = [self.rect.size[1]] + [i.rect.size[1] for i in self.values]
        return self.rect.size[0], sum(sizes)

    @property
    def totalRect(self):
        return pygame.Rect(self.rect.topleft, self.get_size())

    def get_colour(self):
        colour = pygame.Color(0)
        hsla = [int((360/self.pwidth)*self.pwidth*self.p[0]), 100, 100-int(100*self.p[1]), 100]
        for i in self.values:
            hsla[i.type] = int(i.bounds * i.p)
        colour.hsla = tuple(hsla)
        return colour
    
    def set_colour(self, colour):
        hsla = colour.hsla
        self.p = (
                    (hsla[0] / 360) * self.pwidth / self.pwidth,
                    (100 - hsla[2]) / 100
        )
        for i in self.values:
            i.p = hsla[i.type] / i.bounds

    def update(self, mousePos):
        up = False
        for i in self.values:
            up = up or (bool(mousePos) and i.update(mousePos))
        if bool(mousePos) and self.rect.collidepoint(mousePos):
            mouse.Mouse.set(mouse.MouseState.PICK)
            if pygame.mouse.get_pressed()[0] and not up:
                self.p = ((mousePos[0] - self.imrect.left) / self.pwidth, (mousePos[1] - self.imrect.top) / self.pheight)
                self.p = ((max(0, min(self.p[0], 1))), (max(0, min(self.p[1], 1))))

    def draw(self, surf):
        if self.values != []:
            pygame.draw.rect(surf, (255, 255, 255), self.rect, border_radius=8, border_bottom_left_radius=0, border_bottom_right_radius=0)
        else:
            pygame.draw.rect(surf, (255, 255, 255), self.rect, border_radius=8)
        surf.blit(self.image, self.imrect)
        for i in self.values:
            surf.blit(i.get_twod(self.pwidth, self.pheight), self.imrect)
        center = self.imrect.left + self.p[0] * self.pwidth, self.imrect.top + self.p[1] * self.pheight
        for i in self.values:
            i.draw(surf)
        h = self.rect.height
        for i in self.values:
            h += i.rect.height
        pygame.draw.rect(surf, (155, 155, 155), (self.rect.left-4, self.rect.top-4, self.rect.width+8, h+8), border_radius=8, width=8)
        pygame.draw.circle(surf, self.get_colour(), center, 25)

class ColourPickerBTN(Element):
    type = GO.TCOLOURPICK
    def __init__(self, 
                 pos: GO.P___, 
                 size: int = 20, 
                 sizeofpicker: int = 200,
                 default: GO.C___ = (255, 10, 10)
        ):
        """
        A colour picker button :)

        Args:
            pos (GO.P___): The position on the graphic screen this will be positioned in.
            size (int, optional): The size of the button. Defaults to 20.
            sizeofpicker (int, optional): The size of the picker window. Defaults to 200.
            default (GO.C___, optional): The starting colour. Defaults to (255, 10, 10).
        """
        super().__init__(pos, (size, size))
        self.sop = sizeofpicker
        self.picker = ColourPicker(0, 0, border=self.sop//10, w=self.sop)
        self.picker.p = (0, 0.5)
        self.active = False
        self.set(*default)
    
    def get(self):
        """Get the rgb colour of the picker"""
        c = self.picker.get_colour()
        return (c.r, c.g, c.b)
    
    def set(self, r, g, b):
        """Set the rgb colour of the picker"""
        self.picker.set_colour(pygame.Color(r, g, b))
    
    def update(self, mousePos, events, force_redraw=False):
        if not force_redraw:
            return ReturnState.REDRAW
        if self.G.pause:
            self.active = False
        mouse_pressed = pygame.mouse.get_pressed()[0]
        x, y = self.stackP()
        rect = pygame.Rect(x, y, *self.size)
        if not self.G.pause:
            if bool(mousePos) and rect.collidepoint(mousePos):
                if mouse_pressed:
                    mouse.Mouse.set(mouse.MouseState.CLICKING)
                else:
                    mouse.Mouse.set(mouse.MouseState.HOVER)
                if mouse_pressed:
                    s = self.picker.get_size()
                    if x - s[0] < 0 and y - s[1] < 0:
                        self.picker.set_position(x+self.size[0]*2, y+self.size[1]*2)
                    elif x - s[0] < 0:
                        self.picker.set_position(x+self.size[0]*2, y-s[1]+20)
                    elif y - s[1] < 0:
                        self.picker.set_position(x-s[0]+20, y+self.size[1]*2)
                    else:
                        self.picker.set_position(x-s[0]+20, y-s[1]+20)
                    self.active = True
            elif bool(mousePos) and mouse_pressed and not rect.collidepoint(mousePos) and not self.picker.totalRect.collidepoint(mousePos):
                self.active = False
        if self.active:
            self.picker.update(mousePos)
    
    def draw(self):
        x, y = self.stackP()
        rect = pygame.Rect(x, y, *self.size)
        if self.active:
            self.picker.draw(self.G.WIN)
        pygame.draw.rect(self.G.WIN, (0, 0, 0), (x-2, y-2, self.size[0]+4, self.size[1]+4), border_radius=8)
        pygame.draw.rect(self.G.WIN, (255, 255, 255), rect, border_radius=8)
        pygame.draw.rect(self.G.WIN, self.get(), (x+self.size[0]//4, y+self.size[1]//4, self.size[0]-self.size[0]//2, self.size[1]-self.size[1]//2), border_radius=8)
