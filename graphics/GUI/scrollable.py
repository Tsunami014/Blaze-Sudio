import pygame

class Scrollable:
    def __init__(self, sur, pos, goalrect, bounds=(0, float('inf')), outline=10, bar=True, outlinecol=(155, 155, 155)):
        self.sur = sur
        self.bar = bar
        self.pos = pos
        self.goalrect = goalrect
        self.scroll = 0
        self.bounds = bounds
        self.outline = (outline, outlinecol)
    def update(self, event):
        y = event.y - 1
        if 0 <= y <= 1: y = 2
        self.scroll += y * 2
        self.scroll = -min(max(self.bounds[0], -self.scroll), self.bounds[1])
    
    def __call__(self, WIN):
        s = pygame.Surface(self.goalrect)
        s.blit(self.sur, (0, self.scroll))
        WIN.blit(s, self.pos)
        if self.outline[0] != 0: pygame.draw.rect(WIN, self.outline[1], pygame.Rect(*self.pos, *self.goalrect), self.outline[0], 3)
        if self.bar:
            try:
                try: w = self.outline[0]/2
                except ZeroDivisionError: w = 0
                p = (self.pos[0]+self.goalrect[0]-w, self.pos[1]+((-self.scroll) / self.bounds[1])*(self.goalrect[1]-40)+20)
                pygame.draw.line(WIN, (200, 50, 50), (p[0], p[1]-20), (p[0], p[1]+20), 10)
            except: pass

if __name__ == '__main__':
    pygame.init()
    w = pygame.display.set_mode()
    from tkinter.filedialog import askopenfilename
    im = pygame.image.load(askopenfilename(defaultextension='.png', filetypes=[('.png', '.png'), ('.jpg', '.jpg')]))
    S = Scrollable(im, (20, 20), (500, 500), (0, im.get_height()-500))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEWHEEL:
                S.update(event)
        w.fill((0, 0, 0))
        S(w)
        pygame.display.update()
