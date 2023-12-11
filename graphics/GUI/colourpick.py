import pygame

# Thanks to https://stackoverflow.com/questions/73517832/how-to-make-an-color-picker-in-pygame :)

class ColourPicker:
    def __init__(self, x, y):
        self.pwidth = 360
        self.pheight = 100
        self.rect = pygame.Rect(x, y, self.pwidth, self.pheight)
        self.image = pygame.Surface((self.pwidth, self.pheight))
        self.image.fill((255, 255, 255))
        for i in range(self.pwidth):
            for j in range(self.pheight):
                colour = pygame.Color(0)
                colour.hsla = (int(360*i/self.pwidth), 100, 100-j, 100)
                pygame.draw.rect(self.image, colour, (i, j, 1, 1))
        self.p = (0, 0)

    def get_colour(self):
        colour = pygame.Color(0)
        colour.hsla = (int(self.p[0] * self.pwidth), 100, 100-int(self.p[1] * self.pheight), 100)
        return colour

    def update(self):
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0] and self.rect.collidepoint(mouse_pos):
            self.p = ((mouse_pos[0] - self.rect.left) / self.pwidth, (mouse_pos[1] - self.rect.top) / self.pheight)
            self.p = ((max(0, min(self.p[0], 1))), (max(0, min(self.p[1], 1))))

    def draw(self, surf):
        surf.blit(self.image, self.rect)
        center = self.rect.left + self.p[0] * self.pwidth, self.rect.top + self.p[1] * self.pheight
        pygame.draw.circle(surf, self.get_colour(), center, 25)

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    cp = ColourPicker(50, 50)

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
