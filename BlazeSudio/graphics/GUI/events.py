from typing import Callable, Iterable, Literal
import pygame
from math import sqrt
from BlazeSudio.graphics.base import Element, ReturnState
from BlazeSudio.graphics import mouse, options as GO # TODO: Replace more things in here with GO stuff

__all__ = ['Dropdown', 'Toast']

class Dropdown(Element):
    def __init__(self,
                 pos: Iterable[int],
                 elms: Iterable[str], 
                 spacing: int = 5, 
                 font: GO.F___ = GO.FFONT, 
                 bgcolour: GO.C___ = GO.CBLACK, 
                 txtcolour: GO.C___ = GO.CWHITE, 
                 selectedcol: GO.C___ = GO.CBLUE, 
                 pauseG: bool = True,
                 extraW: int = None,
                 func: Callable = lambda selected: None
                ):
        """
        Make a dropdown!

        Args:
            pos (Iterable[int, int]): The position on the screen to spawn this dropdown. Having GO.P___ is kinda weird for this...
            elms (Iterable[str]): The elements present in the dropdown to choose from.
            spacing (int, optional): The spacing between the text and the outside of their enclosing rects. Defaults to 5.
            font (GO.F___, optional): The font to render the text with. Defaults to GO.FFONT.
            bgcolour (GO.C___, optional): The colour of the background of the dropdown. Defaults to GO.CBLACK.
            txtcolour (GO.C___, optional): The colour of the text inside the dropdown. Defaults to GO.CWHITE.
            selectedcol (GO.C___, optional): The colour of the selection highlight. Defaults to GO.CBLUE.
            pauseG (bool, optional): Whether to pause the graphic screen when the dropdown is active. Defaults to True.
            extraW (int, optional): Extra width to add to the dropdown. Defaults to None.
            func (Callable, optional): The function to call when an option is selected. Defaults to a do nothing func. \
                Func *must* have an input argument which will be the id of the selected element in the list that was selected or None if nothing was selected.
        """
        self.pauseG = pauseG
        self.spacing = spacing
        self.elements = [font.render(i, txtcolour) for i in elms]
        mx = max([i.get_width() + spacing*2 for i in self.elements]+[extraW or 0])
        my = sum([i.get_height() + spacing*2 for i in self.elements])
        self.bgcolour = bgcolour
        self.selectedcol = selectedcol
        self.func = func
        self.rects = []
        y = 0
        for i in self.elements:
            sze = i.get_size()
            sze = (mx, sze[1] + self.spacing*2)
            self.rects.append(pygame.Rect(pos[0], pos[1]+y, *sze))
            y += sze[1]
        super().__init__(GO.PSTATIC(*pos), (mx, my))
    
    def _init2(self):
        if self.pauseG:
            self.G.pause = True
        super()._init2()
    
    def update(self, mousePos, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                self.G.pause = False
                ran = False
                for i in range(len(self.rects)):
                    if self.rects[i].collidepoint(*mousePos.pos):
                        self.func(i)
                        ran = True
                        break
                if not ran:
                    self.func(None)
                self.remove()
                return ReturnState.REDRAW_HIGHEST
        
        return ReturnState.REDRAW_HIGHEST
    
    def draw(self, mousePos):
        pygame.draw.rect(self.G.WIN, self.bgcolour, pygame.Rect(*self.stackP(), *self.size), border_radius=8)
        for i in range(len(self.rects)):
            if self.rects[i].collidepoint(*mousePos.pos):
                if pygame.mouse.get_pressed()[0]:
                    mouse.Mouse.set(mouse.MouseState.CLICKING)
                else:
                    mouse.Mouse.set(mouse.MouseState.HOVER)
                pygame.draw.rect(self.G.WIN, self.selectedcol, self.rects[i], border_radius=8)
            p = self.rects[i].topleft
            self.G.WIN.blit(self.elements[i], (p[0] + self.spacing, p[1] + self.spacing))

class Toast(Element):
    type = GO.TTOAST
    def __init__(self, 
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
        super().__init__(pos, sur.get_size())
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
        if self.goto != self.curPos:
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
        return ReturnState.REDRAW_HIGHEST

    def draw(self):
        ns = self.surf
        if self.goto != self.curPos:
            if self.living:
                ns.set_alpha(255-self.initdist*self.dist())
            else:
                ns.set_alpha(self.initdist*self.dist())
        self.G.WIN.blit(ns, self.curPos)
