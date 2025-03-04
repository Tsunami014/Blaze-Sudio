import pygame
from functools import lru_cache
from BlazeSudio.graphics.base import Element
from BlazeSudio.graphics import options as GO

class Player(Element):
    def __init__(self, world):
        self.world = world
        super().__init__(GO.PLTOP, (0, 0))
    
    def _init2(self):
        self.size = self.G.size
        super()._init2()

    def update(self, mPos, events):
        self.G.curScene.tick(events.copy())
    
    @lru_cache
    def _find_bg(self, bg, col, nsize):
        if bg is not None:
            return pygame.transform.scale(bg, nsize)
        else:
            newSur = pygame.Surface(nsize, pygame.SRCALPHA)
            newSur.fill(col)
            return newSur

    def draw(self):
        rend = self.G.curScene.render()
        if not self.G.curScene.useRenderer:
            return
        rend = self.G.curScene.postProcessGlobal(rend)
        win = self.G.WIN
        sze = self.G.size
        mw, mh = sze[0] / 2, sze[1] / 2

        scale = self.G.curScene.CamDist
        realpos = self.G.curScene.CamPos
        realpos = [realpos[0] * scale, realpos[1] * scale]
        
        sur = rend
        
        bounds = self.G.curScene.CamBounds
        
        # Calculate diff_x
        if sur.get_width() * scale < sze[0] or (bounds[0] is None and bounds[2] is None):
            diff_x = realpos[0]
        else:
            if bounds[0] is None:
                diff_x = min(realpos[0], bounds[2]*scale-mw)
            elif bounds[2] is None:
                diff_x = max(realpos[0], bounds[0]*scale+mw)
            else:
                diff_x = max(min(realpos[0], bounds[2]*scale-mw), bounds[0]*scale+mw)
        
        # Calculate diff_y
        if sur.get_height() * scale < sze[1] or (bounds[1] is None and bounds[3] is None):
            diff_y = realpos[1]
        else:
            if bounds[1] is None:
                diff_y = min(realpos[1], bounds[3]*scale-mh)
            elif bounds[3] is None:
                diff_y = max(realpos[1], bounds[1]*scale+mh)
            else:
                diff_y = max(min(realpos[1], bounds[3]*scale-mh), bounds[1]*scale+mh)
        
        ndiff_x = mw - diff_x
        ndiff_y = mh - diff_y

        newSur = self._find_bg(self.G.currentLvL.bgPic, self.G.currentLvL.bgColour, (sze[0]/scale, sze[1]/scale)).copy()
        newSur.blit(sur, (ndiff_x/scale, ndiff_y/scale))

        rendSur = pygame.transform.scale(self.G.curScene.postProcessScreen(newSur, (diff_x, diff_y)), sze)

        win.blit(
            rendSur, 
            (0, 0)
        )
