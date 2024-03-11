import pygame
from math import sqrt

def dropdown(win, elms, spacing=5, font=None, bgcolour=(0, 0, 0), txtcolour=(255, 255, 255), selectedcol=(0, 0, 255), mpos=None):
    if font == None: font = pygame.font.SysFont(None, 30)
    elements = [font.render(i, txtcolour) for i in elms]
    mx = max([i.get_width() + spacing*2 for i in elements])
    my = sum([i.get_height() + spacing*2 for i in elements])
    rects = []
    if mpos == None: mpos = pygame.mouse.get_pos()
    pos = mpos
    for i in elements:
        sze = i.get_size()
        sze = (mx, sze[1] + spacing*2)
        rects.append(pygame.Rect(*pos, *sze))
        pos = (pos[0], pos[1] + sze[1])
    sur = win.copy()
    while True:
        win.fill((255, 255, 255))
        win.blit(sur, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                for i in range(len(rects)):
                    if rects[i].collidepoint(*pygame.mouse.get_pos()):
                        return i
                return None
        pygame.draw.rect(win, bgcolour, pygame.Rect(*mpos, mx, my), border_radius=8)
        for i in range(len(rects)):
            if rects[i].collidepoint(*pygame.mouse.get_pos()):
                pygame.draw.rect(win, selectedcol, rects[i], border_radius=8)
            p = rects[i].topleft
            win.blit(elements[i], (p[0] + spacing, p[1] + spacing))
        pygame.display.update()

class Toast:
    def __init__(self, surf, pos, bottompos, timeout):
        rnd = lambda inp: [round(inp[0]), round(inp[1])]
        self.surf = surf
        self.pos = rnd(bottompos)
        self.end = rnd(bottompos)
        self.goto = rnd(pos)
        self.initdist = 255 / self.dist()
        self.timeout = timeout
        self.time = 0
        self.living = True
    
    def dist(self):
        return sqrt((self.goto[0] - self.pos[0])**2 + (self.goto[1] - self.pos[1])**2)
    
    def update(self, WIN):
        self.time += 1
        ns = self.surf
        if self.goto != self.pos:
            if self.living: ns.set_alpha(255-self.initdist*self.dist())
            else: ns.set_alpha(self.initdist*self.dist())
            if self.goto[0] != self.pos[0]:
                if self.pos[0] > self.goto[0]: self.pos[0] -= 1
                else: self.pos[0] += 1
            if self.goto[1] != self.pos[1]:
                if self.pos[1] > self.goto[1]: self.pos[1] -= 1
                else: self.pos[1] += 1
        else:
            if not self.living:
                return False
        if self.time > self.timeout and self.living:
            self.pos = self.goto
            self.goto = self.end
            self.living = False
        WIN.blit(ns, self.pos)
        return True
