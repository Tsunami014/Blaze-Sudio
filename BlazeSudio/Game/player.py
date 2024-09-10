import pygame
import BlazeSudio.graphics.options as GO
import BlazeSudio.Game.statics as statics

class Player:
    def __init__(self, G, world, Game):
        self.Game = Game
        self.G = G
        self.world = world

    def update(self, events, mPos):
        win = self.G.WIN
        sze = self.G.size
        keys = pygame.key.get_pressed()
        
        self.Game.curScene.tick(keys)
        
        scale = self.Game.curScene.CamDist()
        pos = self.Game.curScene.CamPos()
        
        win.fill(self.Game.currentLvL._bgColor)
        sur = self.Game.curScene.render()
        sur = pygame.transform.scale(sur, (sur.get_width() * scale, sur.get_height() * scale))
        
        bounds = self.Game.curScene.CamBounds()

        # Apply bounds to position
        if bounds[0] is not None:
            pos[0] = max(pos[0], bounds[0])
        if bounds[2] is not None:
            pos[0] = min(pos[0], bounds[2])
        if bounds[1] is not None:
            pos[1] = max(pos[1], bounds[1])
        if bounds[3] is not None:
            pos[1] = min(pos[1], bounds[3])

        # TODO: Not need the 'self.Game.currentLvL.layerInstances[0]['__gridSize']'
        # Calculate real position
        realpos = ((pos[0] * self.Game.currentLvL.layerInstances[0]['__gridSize']) * scale,
                (pos[1] * self.Game.currentLvL.layerInstances[0]['__gridSize']) * scale)

        mw, mh = sze[0] / 2, sze[1] / 2

        # Zero Check
        ZC = lambda x: (0 if x < 0 else x)

        if sur.get_width() < sze[0] or (bounds[0] is None and bounds[2] is None):
            diff_x = 0
        else:
            if bounds[0] is None:
                diff_x = -ZC(realpos[0] - (sur.get_width() - mw))
            elif bounds[2] is None:
                diff_x = ZC(mw - realpos[0])
            else:
                diff_x = ZC(mw - realpos[0]) or -ZC(realpos[0] - (sur.get_width() - mw))
        
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

        playersze = self.Game.currentLvL.layerInstances[0]['__gridSize'] * scale
        self.Game.curScene.renderUI(win, (diff_x, diff_y), (mw, mh), playersze)
