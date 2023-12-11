import pygame

# Thanks to https://stackoverflow.com/questions/73517832/how-to-make-an-color-picker-in-pygame :)

class ColourPicker:
    def __init__(self, x, y, border=5, w=100, h=None):
        self.pwidth = w
        self.pheight = h or w
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
        colour.hsla = (int((360/self.pwidth)*self.pwidth*self.p[0]), 100, 100-int(100*self.p[1]), 100)
        return colour

    def update(self):
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0] and self.imrect.collidepoint(mouse_pos):
            self.p = ((mouse_pos[0] - self.imrect.left) / self.pwidth, (mouse_pos[1] - self.imrect.top) / self.pheight)
            self.p = ((max(0, min(self.p[0], 1))), (max(0, min(self.p[1], 1))))

    def draw(self, surf):
        surf.fill((255, 255, 255), self.rect)
        surf.blit(self.image, self.imrect)
        center = self.imrect.left + self.p[0] * self.pwidth, self.imrect.top + self.p[1] * self.pheight
        pygame.draw.circle(surf, self.get_colour(), center, 25)

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    cp = ColourPicker(50, 50, 20, 200)

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
