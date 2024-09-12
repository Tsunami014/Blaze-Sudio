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

        # Zero Check
        ZC = lambda x: (0 if x < 0 else x)

        # TODO: I have no idea what's going on
        if sur.get_width() < sze[0] or (bounds[0] is None and bounds[2] is None):
            diff_x = 0
        else:
            if bounds[0] is None:
                d = realpos[0] - (sur.get_width() - mw)
                diff_x = -(bounds[2] if d < bounds[2] else d)
            elif bounds[2] is None:
                d = mw - realpos[0]
                diff_x = (bounds[0] if d < bounds[0] else d)
            else:
                d1 = mw - realpos[0]
                if d1 < bounds[0]:
                    diff_x = bounds[0]
                else:
                    d2 = realpos[0] - (sur.get_width() - mw)
                    diff_x = -(bounds[2] if d2 < bounds[2] else d2)
        
        if sur.get_height() < sze[1] or (bounds[1] is None and bounds[3] is None):
            diff_y = 0
        else:
            if bounds[1] is None:
                diff_y = -ZC(realpos[1] - (sur.get_height() - mh))
            elif bounds[3] is None:
                diff_y = ZC(mh - realpos[1])
            else:
                diff_y = ZC(mh - realpos[1]) or -ZC(realpos[1] - (sur.get_height() - mh))

        # Blit the surface considering the camera bounds and diffs
        win.blit(sur, [
            -realpos[0] + mw - diff_x,
            -realpos[1] + mh - diff_y
        ])

        playersze = scale
        self.Game.curScene.renderUI(win, (diff_x, diff_y), (mw, mh), playersze)
