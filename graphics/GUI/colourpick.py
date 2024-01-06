import pygame

# Thanks to https://stackoverflow.com/questions/73517832/how-to-make-an-color-picker-in-pygame :)

class ValuePicker:
    def __init__(self, x, y, w, h, default=0, type=0, border=False):
        self.size = (w, h)
        self.type = type
        self.border = border
        self.bounds = 360 if type == 0 else 100
        self.rad = h//2
        self.pwidth = w-self.rad*2
        self.rect = pygame.Rect(x, y, w, h)
        self.imrect = pygame.Rect(x+h//2, y+h//3, self.pwidth, h-2*h//3)
        self.image = pygame.Surface((self.pwidth, h-2*h//3))
        self.image.fill((255, 255, 255))
        for i in range(self.pwidth):
            colour = pygame.Color(0)
            hsla = [360, 100, 50, 100]
            hsla[self.type] = int(self.bounds*i/self.pwidth)
            colour.hsla = tuple(hsla)
            pygame.draw.rect(self.image, colour, (i, 0, 1, h-2*h//3))
        try: self.p = (1/self.bounds)*default
        except: self.p = 0
        self.twod = pygame.Surface((self.pwidth, self.pwidth))
        self.twod.fill((255, 255, 255))
        for i in range(self.pwidth):
            for j in range(self.pwidth):
                try:
                    colour = pygame.Color(0)
                    hsla = [360, 100, 100-int((100/self.pwidth)*j*2*(100/self.pwidth)), 100]
                    hsla[self.type] = 0
                    colour.hsla = tuple(hsla)
                    pygame.draw.rect(self.twod, colour, (i, j, 1, 1))
                except: pass
        self.p = (max(0, min(self.p, 1)))
    
    def set_position(self, x, y):
        h = self.size[1]
        self.rect = pygame.Rect(x, y, *self.size)
        self.imrect = pygame.Rect(x+h//2, y+h//3, self.pwidth, h-2*h//3)
    
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

    def update(self, mp=pygame.mouse.get_pos):
        moude_buttons = pygame.mouse.get_pressed()
        mouse_pos = mp()
        if moude_buttons[0] and self.rect.collidepoint(mouse_pos):
            self.p = (mouse_pos[0] - self.rect.left - self.rad) / self.pwidth
            self.p = (max(0, min(self.p, 1)))
            return True
        return False

    def draw(self, surf):
        if not self.border:
            pygame.draw.rect(surf, (255, 255, 255), self.rect)
        else: pygame.draw.rect(surf, (255, 255, 255), self.rect, border_radius=8, border_top_left_radius=0, border_top_right_radius=0)
        surf.blit(self.image, self.imrect)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pygame.draw.circle(surf, self.get_colour(), center, self.rect.height // 2)

class ColourPicker:
    def __init__(self, x, y, border=5, values=[1], w=100, h=None):
        self.pwidth = w
        self.pheight = h or w
        self.values = [ValuePicker(x-border, y+self.pheight+border+i*50, w+border*2, 50, [0, 100, 50, 100][values[i]], values[i], i==len(values)-1) for i in range(len(values))]
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
                except: pass
        self.p = (0, 0)
    
    def set_position(self, x, y):
        
        for i in range(len(self.values)):
            self.values[i].set_position(x-self.border, y+self.pheight+self.border+i*50)
        
        self.rect = pygame.Rect(x-self.border, y-self.border, self.pwidth+self.border*2, self.pheight+self.border*2)
        self.imrect = pygame.Rect(x, y, self.pwidth, self.pheight)
    
    def get_size(self):
        sizes = [self.rect.size[1]] + [i.rect.size[1] for i in self.values]
        return self.rect.size[0], sum(sizes)

    def get_colour(self):
        colour = pygame.Color(0)
        hsla = [int((360/self.pwidth)*self.pwidth*self.p[0]), 100, 100-int(100*self.p[1]), 100]
        for i in self.values:
            hsla[i.type] = int(i.bounds * i.p)
        colour.hsla = tuple(hsla)
        return colour

    def update(self, mp=pygame.mouse.get_pos):
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = mp()
        up = False
        for i in self.values: up = up or i.update(mp)
        if mouse_buttons[0] and self.rect.collidepoint(mouse_pos) and not up:
            self.p = ((mouse_pos[0] - self.imrect.left) / self.pwidth, (mouse_pos[1] - self.imrect.top) / self.pheight)
            self.p = ((max(0, min(self.p[0], 1))), (max(0, min(self.p[1], 1))))

    def draw(self, surf):
        if self.values != []:
            pygame.draw.rect(surf, (255, 255, 255), self.rect, border_radius=8, border_bottom_left_radius=0, border_bottom_right_radius=0)
        else: pygame.draw.rect(surf, (255, 255, 255), self.rect, border_radius=8)
        surf.blit(self.image, self.imrect)
        for i in self.values:
            surf.blit(i.get_twod(self.pwidth, self.pheight), self.imrect)
        center = self.imrect.left + self.p[0] * self.pwidth, self.imrect.top + self.p[1] * self.pheight
        for i in self.values: i.draw(surf)
        h = self.rect.height
        for i in self.values: h += i.rect.height
        pygame.draw.rect(surf, (155, 155, 155), (self.rect.left-4, self.rect.top-4, self.rect.width+8, h+8), border_radius=8, width=8)
        pygame.draw.circle(surf, self.get_colour(), center, 25)

class ColourPickerBTN:
    def __init__(self, win, x, y, size=20, sizeofpicker=200):
        self.win = win
        self.sop = sizeofpicker
        self.size = size
        self.pos = (x, y)
        self.picker = ColourPicker(0, 0, border=self.sop//10, w=self.sop)
        self.picker.p = (0, 0.5)
        self.active = False
    
    def get_colour(self):
        return self.picker.get_colour()
    def get(self):
        c = self.get_colour()
        return (c.r, c.b, c.g)
    
    def update(self, mp=pygame.mouse.get_pos):
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = mp()
        rect = pygame.Rect(*self.pos, self.size, self.size)
        if mouse_buttons[0] and rect.collidepoint(mouse_pos):
            s = self.picker.get_size()
            if self.pos[0] - s[0] < 0 and self.pos[1] - s[1] < 0:
                self.picker.set_position(self.pos[0]+self.size*2, self.pos[1]+self.size*2)
            elif self.pos[0] - s[0] < 0:
                self.picker.set_position(self.pos[0]+self.size*2, self.pos[1]-s[1]+20)
            elif self.pos[1] - s[1] < 0:
                self.picker.set_position(self.pos[0]-s[0]+20, self.pos[1]+self.size*2)
            else:
                self.picker.set_position(self.pos[0]-s[0]+20, self.pos[1]-s[1]+20)
            self.active = True
        elif mouse_buttons[0] and not rect.collidepoint(mouse_pos) and not pygame.Rect(self.picker.rect.x, self.picker.rect.y, *self.picker.get_size()).collidepoint(mouse_pos):
            self.active = False
        if self.active:
            self.picker.update(mp)
        self.draw()
    
    def draw(self):
        if self.active:
            self.picker.draw(self.win)
        pygame.draw.rect(self.win, (0, 0, 0), (self.pos[0]-2, self.pos[1]-2, self.size+4, self.size+4), border_radius=8)
        pygame.draw.rect(self.win, (255, 255, 255), pygame.Rect(*self.pos, self.size, self.size), border_radius=8)
        pygame.draw.rect(self.win, self.get_colour(), (self.pos[0]+self.size//4, self.pos[1]+self.size//4, self.size-self.size//2, self.size-self.size//2), border_radius=8)

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    cp = ColourPickerBTN(window, 50, 50)

    run = True
    while run:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[2]:
            mp = pygame.mouse.get_pos()
            cp.pos = (mp[0]-cp.size//2, mp[1]-cp.size//2)

        window.fill(0)
        cp.update()
        pygame.display.flip()
        
    pygame.quit()
    exit()
