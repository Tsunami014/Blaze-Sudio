import pygame
from BlazeSudio.graphics.GUI.elements import Element, ReturnState
import BlazeSudio.graphics.options as GO
# TODO: rename this file

class Static(Element):
    type = GO.TSTATIC
    def __init__(self, G, sur, pos):
        super().__init__(G)
        self.sur = sur
        self.pos = pos
    
    def get(self):
        """Get the surface and position"""
        return self.sur, self.pos
    
    def update(self, mpos, events):
        self.G.WIN.blit(self.sur, self.pos)


class Button(Element):
    type = GO.TBUTTON
    def __init__(self, G, rect, pos, col, sur, txt, on_hover_enlarge):
        super().__init__(G)
        self.rect = rect
        self.pos = pos
        self.col = col
        self.sur = sur
        self.txt = txt
        self.OHE = on_hover_enlarge
    
    def get(self):
        """Get the text on the button"""
        return self.txt
    
    def update(self, mousePos, events, force_draw=False):
        r = self.rect.copy()
        if not self.G.pause:
            if r.collidepoint(mousePos):
                if self.OHE != -1:
                    r.x -= self.OHE
                    r.y -= self.OHE
                    r.width += self.OHE*2
                    r.height += self.OHE*2
                if not force_draw:
                    if any([i.type == pygame.MOUSEBUTTONDOWN for i in events]):
                        return ReturnState.CALL + ReturnState.TBUTTON
                    return ReturnState.TBUTTON
        pygame.draw.rect(self.G.WIN, self.col, r, border_radius=8)
        self.G.WIN.blit(self.sur, (self.pos[0]+10, self.pos[1]+10))