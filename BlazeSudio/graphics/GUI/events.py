import pygame
from math import sqrt
from BlazeSudio.graphics.GUI.elements import Element
import BlazeSudio.graphics.options as GO # TODO: Replace more things in here with GO stuff

__all__ = ['dropdown', 'Toast']

def dropdown(G, elms, spacing=5, font=None, bgcolour=(0, 0, 0), txtcolour=(255, 255, 255), selectedcol=(0, 0, 255), mpos=None):
    win = G.WIN
    if font is None:
        font = pygame.font.SysFont(None, 30)
    elements = [font.render(i, txtcolour) for i in elms]
    mx = max([i.get_width() + spacing*2 for i in elements])
    my = sum([i.get_height() + spacing*2 for i in elements])
    rects = []
    if mpos is None:
        mpos = pygame.mouse.get_pos()
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

class Toast(Element):
    type = GO.TTOAST
    def __init__(self, G, text, BGcol, txtcol=GO.CBLACK, font=GO.FFONT, pos=GO.PCBOTTOM, spacing=5, dist=20, timeout=120):
        txt = font.render(text, txtcol)
        sur = pygame.Surface((txt.get_size()[0]+spacing*2, txt.get_size()[1]+spacing*2), pygame.SRCALPHA)
        sur.fill((0, 0, 0, 0))
        pygame.draw.rect(sur, BGcol, pygame.Rect(0, 0, *sur.get_size()), border_radius=8)
        sur.blit(txt, (spacing, spacing))
        pos = pos.copy()
        super().__init__(G, pos, sur.get_size())
        self.surf = sur
        endpos = self.stackP()
        bottompos = (endpos[0]+pos.stack[0]*sur.get_width(), endpos[1]+pos.stack[1]*sur.get_height())
        endpos = (endpos[0]-pos.stack[0]*dist, endpos[1]-pos.stack[1]*dist)
        self.curPos = list(bottompos)
        self.end = list(bottompos)
        self.goto = list(endpos)
        self.initdist = 255 / self.dist()
        self.timeout = timeout
        self.time = 0
        self.living = True
    
    def get(self):
        """Get the time through the animation"""
        return self.time
    
    def set(self, t):
        """Set the time through the animation"""
        self.time = t
    
    def dist(self):
        return sqrt((self.goto[0] - self.curPos[0])**2 + (self.goto[1] - self.curPos[1])**2)
    
    def update(self, mousePos, events):
        self.time += 1
        ns = self.surf
        if self.goto != self.curPos:
            if self.living:
                ns.set_alpha(255-self.initdist*self.dist())
            else:
                ns.set_alpha(self.initdist*self.dist())
            if self.goto[0] != self.curPos[0]:
                if round(self.curPos[0]) > round(self.goto[0]):
                    self.curPos[0] -= 1
                elif round(self.curPos[0]) < round(self.goto[0]):
                    self.curPos[0] += 1
                else:
                    self.curPos[0] = self.goto[0]
            if self.goto[1] != self.curPos[1]:
                if round(self.curPos[1]) > round(self.goto[1]):
                    self.curPos[1] -= 1
                elif round(self.curPos[1]) < round(self.goto[1]):
                    self.curPos[1] += 1
                else:
                    self.curPos[1] = self.goto[1]
        else:
            if not self.living:
                self.remove()
        if self.time > self.timeout and self.living:
            self.curPos = self.goto
            self.goto = self.end
            self.living = False
        self.G.WIN.blit(ns, self.curPos)
