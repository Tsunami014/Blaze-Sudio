import pygame
import BlazeSudio.graphics.options as GO
import BlazeSudio.Game.statics as statics

class Player:
    def __init__(self, G, world, Game):
        self.Game = Game
        self.G = G
        self.world = world

    def update(self, mPos, events):
        self.Game.curScene.tick(events.copy())
        rend = self.Game.curScene.render()
        if not self.Game.curScene.useRenderer:
            return
        win = self.G.WIN
        sze = self.G.size
        mw, mh = sze[0] / 2, sze[1] / 2
        
        scale = self.Game.curScene.CamDist
        realpos = self.Game.curScene.CamPos
        realpos = [realpos[0] * scale, realpos[1] * scale]
        
        win.fill(self.Game.currentLvL.bgColour)
        sur = rend or pygame.Surface((0, 0))
        sur = pygame.transform.scale(sur, (sur.get_width() * scale, sur.get_height() * scale))
        
        bounds = self.Game.curScene.CamBounds
        
        # Calculate diff_x
        if sur.get_width() < sze[0] or (bounds[0] is None and bounds[2] is None):
            diff_x = realpos[0]
        else:
            if bounds[0] is None:
                diff_x = min(realpos[0], bounds[2]*scale-mw)
            elif bounds[2] is None:
                diff_x = max(realpos[0], bounds[0]*scale+mw)
            else:
                diff_x = max(min(realpos[0], bounds[2]*scale-mw), bounds[0]*scale+mw)
        
        # Calculate diff_y
        if sur.get_height() < sze[1] or (bounds[1] is None and bounds[3] is None):
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
        
        # Blit the surface considering the camera bounds and diffs
        win.blit(sur, [diff_x, diff_y])

        self.Game.curScene.renderUI(win, (diff_x, diff_y), (mw, mh), scale) # TODO: Make this so much better
