import pygame

# Thanks to https://stackoverflow.com/questions/73517832/how-to-make-an-color-picker-in-pygame :)

class ValuePicker:
    def __init__(self, x, y, w, h, default=0, type=0):
        self.type = type
        self.bounds = 360 if type == 0 else 100
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface((w, h))
        self.image.fill((255, 255, 255))
        self.rad = h//2
        self.pwidth = w-self.rad*2
        for i in range(self.pwidth):
            colour = pygame.Color(0)
            hsla = [360, 100, 50, 100]
            hsla[self.type] = int(self.bounds*i/self.pwidth)
            colour.hsla = tuple(hsla)
            pygame.draw.rect(self.image, colour, (i+self.rad, h//3, 1, h-2*h//3))
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

    def update(self):
        moude_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if moude_buttons[0] and self.rect.collidepoint(mouse_pos):
            self.p = (mouse_pos[0] - self.rect.left - self.rad) / self.pwidth
            self.p = (max(0, min(self.p, 1)))
            return True
        return False

    def draw(self, surf):
        surf.blit(self.image, self.rect)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pygame.draw.circle(surf, self.get_colour(), center, self.rect.height // 2)

class ColourPicker:
    def __init__(self, x, y, border=5, values=[1], w=100, h=None):
        self.pwidth = w
        self.pheight = h or w
        self.values = [False if values[i]==None else ValuePicker(x-border, self.pheight+45+border+i*50, w+border*2, 50, [0, 100, 50, 100][values[i]], values[i]) for i in range(len(values))]
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

    def get_colour(self):
        colour = pygame.Color(0)
        hsla = [int((360/self.pwidth)*self.pwidth*self.p[0]), 100, 100-int(100*self.p[1]), 100]
        for i in self.values:
            hsla[i.type] = int(i.bounds * i.p)
        colour.hsla = tuple(hsla)
        return colour

    def update(self):
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        up = False
        for i in self.values: up = up or i.update()
        if mouse_buttons[0] and self.rect.collidepoint(mouse_pos) and not up:
            self.p = ((mouse_pos[0] - self.imrect.left) / self.pwidth, (mouse_pos[1] - self.imrect.top) / self.pheight)
            self.p = ((max(0, min(self.p[0], 1))), (max(0, min(self.p[1], 1))))

    def draw(self, surf):
        surf.fill((255, 255, 255), self.rect)
        surf.blit(self.image, self.imrect)
        for i in self.values:
            surf.blit(i.get_twod(self.pwidth, self.pheight), self.imrect)
        center = self.imrect.left + self.p[0] * self.pwidth, self.imrect.top + self.p[1] * self.pheight
        for i in self.values: i.draw(surf)
        pygame.draw.circle(surf, self.get_colour(), center, 25)

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    cp = ColourPicker(50, 50, 20, w=200)

    run = True
    while run:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 

        cp.update()

        window.fill(0)
        cp.draw(window)
        pygame.display.flip()
        
    pygame.quit()
    exit()
