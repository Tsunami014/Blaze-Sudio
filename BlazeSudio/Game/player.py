import pygame
from functools import lru_cache
from BlazeSudio.graphics.GUI.base import Element
from BlazeSudio.graphics import options as GO

class Player(Element):
    def __init__(self, Game, world):
        self.Game = Game
        self.world = world
        super().__init__(Game, GO.PLTOP, Game.size)

    def update(self, mPos, events):
        self.Game.curScene.tick(events.copy())
    
    @lru_cache
    def _find_bg(self, bg, col, nsize):
        if bg is not None:
            return pygame.transform.scale(bg, nsize)
        else:
            newSur = pygame.Surface(nsize, pygame.SRCALPHA)
            newSur.fill(col)
            return newSur

    def draw(self):
        rend = self.Game.curScene.render()
        if not self.Game.curScene.useRenderer:
            return
        rend = self.Game.curScene.postProcessGlobal(rend)
        win = self.Game.WIN
        sze = self.Game.size
        mw, mh = sze[0] / 2, sze[1] / 2

        scale = self.Game.curScene.CamDist
        realpos = self.Game.curScene.CamPos
        realpos = [realpos[0] * scale, realpos[1] * scale]
        
        sur = rend
        
        bounds = self.Game.curScene.CamBounds
        
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
        
        diff_x = mw - diff_x
        diff_y = mh - diff_y

        newSur = self._find_bg(self.Game.currentLvL.bgPic, self.Game.currentLvL.bgColour, (sze[0]/scale, sze[1]/scale)).copy()
        newSur.blit(sur, (diff_x/scale, diff_y/scale))

        rendSur = pygame.transform.scale(self.Game.curScene.postProcessScreen(newSur), sze)

        win.blit(
            rendSur, 
            (0, 0)
        )

        def scalef(pos):
            return (pos[0]*scale+diff_x, pos[1]*scale+diff_y)

        self.Game.curScene.renderUI(win, scalef)
