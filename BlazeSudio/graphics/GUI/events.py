from typing import Iterable, Literal
import pygame
from math import sqrt
from BlazeSudio.graphics.GUI.base import Element
import BlazeSudio.graphics.options as GO # TODO: Replace more things in here with GO stuff

__all__ = ['dropdown', 'Toast']

def dropdown(G, 
             elms: list[str], 
             spacing: int = 5, 
             font: GO.F___ = GO.FFONT, 
             bgcolour: GO.C___ = GO.CBLACK, 
             txtcolour: GO.C___ = GO.CWHITE, 
             selectedcol: GO.C___ = GO.CBLUE, 
             mpos: Iterable[int] = None
            ) -> None|Literal[False]|int:
    """
    Make a dropdown! A better way to do this is through `Graphic.Dropdown` which is preferrable as it also handles exiting.

    This will stop anything from occuring until the dropdown has finished.

    Args:
        G (Graphic): The graphic screen to attach to.
        elms (list[str]): The elements present in the dropdown to choose from.
        spacing (int, optional): The spacing between the text and the outside of their enclosing rects. Defaults to 5.
        font (GO.F___, optional): The font to render the text with. Defaults to GO.FFONT.
        bgcolour (GO.C___, optional): The colour of the background of the dropdown. Defaults to GO.CBLACK.
        txtcolour (GO.C___, optional): The colour of the text inside the dropdown. Defaults to GO.CWHITE.
        selectedcol (GO.C___, optional): The colour of the selection highlight. Defaults to GO.CBLUE.
        mpos (Iterable[int], optional): The place to spawn the dropdown on. Defaults to the current mouse position.

    Returns:
        None|False|int: 
         - None if clicked out
         - False if quit program
         - int of the idx of the selected element in the input list if selected.
    """
    win = G.WIN
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
    def __init__(self, 
                 G, 
                 text: str, 
                 BGcol: GO.C___ = GO.CORANGE, 
                 txtcol: GO.C___ = GO.CBLACK, 
                 font: GO.F___ = GO.FFONT, 
                 pos: GO.P___ = GO.PCBOTTOM, 
                 spacing: int = 5, 
                 dist: int = 20, 
                 speed: int = 2,
                 timeout: int = 120
                ):
        """
        A Toast; or popup message.

        Args:
            G (Graphic): The graphic screen to attach to.
            text (str): The text in the toast.
            BGcol (GO.C___, optional): The colour of the background of the toast. Defaults to GO.CORANGE.
            txtcol (GO.C___, optional): The colour of the text inside the toast. Defaults to GO.CBLACK.
            font (GO.F___, optional): The font of the toast's text. Defaults to GO.FFONT.
            pos (GO.P___, optional): The position where the toast is in the screen. Defaults to GO.PCBOTTOM.
            spacing (int, optional): The spacing between the text and the outer edge of the toast. Defaults to 5.
            dist (int, optional): The distance inwards to travel from `pos`. Defaults to 20.
            speed (int, optional): How many pixels the toast will move in a frame. Defaults to 2.
            timeout (int, optional): The amount of time the toast will remain on the screen in frames. Defaults to 120.
        """
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
        self.speed = speed
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
                    self.curPos[0] -= self.speed
                elif round(self.curPos[0]) < round(self.goto[0]):
                    self.curPos[0] += self.speed
                else:
                    self.curPos[0] = self.goto[0]
            if self.goto[1] != self.curPos[1]:
                if round(self.curPos[1]) > round(self.goto[1]):
                    self.curPos[1] -= self.speed
                elif round(self.curPos[1]) < round(self.goto[1]):
                    self.curPos[1] += self.speed
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
