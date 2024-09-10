from math import sqrt, ceil
import pygame
import BlazeSudio.graphics.options as GO
import BlazeSudio.Game.statics as statics

class Player:
    def __init__(self, G, world, Game):
        self.Game = Game
        self.G = G
        self.world = world
        self.sur = None
    
    def load_sur(self):
        resp = self.Game.curScene.render()
        if resp is None:
            return False
        self.sur = resp
        return True

    def update(self, events, mPos):
        if self.sur is None:
            self.load_sur()
        win = self.G.WIN
        sze = self.G.size
        keys = pygame.key.get_pressed()
        
        self.Game.curScene.tick(keys)

        scale = self.Game.curScene.CamDist()
        pos = self.Game.curScene.CamPos()
        
        sur = pygame.transform.scale(self.sur, (self.sur.get_width()*scale, self.sur.get_height()*scale))

        # TODO: replace the changing of the level to work with the ldtk neighbours thing and implement that in world.py
        realpos = ((pos[0] * self.Game.currentLvL.layerInstances[0]['__gridSize']) * scale, 
                   (pos[1] * self.Game.currentLvL.layerInstances[0]['__gridSize']) * scale)
        if realpos[0] > sur.get_width():
            self.lvl += 1
            if self.load_sur():
                pos[0] = 0.1
            else: # It failed
                self.lvl -= 1
        elif realpos[0] < 0:
            self.lvl -= 1
            if self.load_sur():
                pos[0] = self.Game.currentLvL.layerInstances[0]['__cWid']-0.1
            else: # It failed
                self.lvl += 1
        if realpos[1] < 0:
            oldlvl = self.lvl
            self.lvl -= ceil(sqrt(len(self.world.ldtk.levels)))
            if self.load_sur():
                pos[1] = self.Game.currentLvL.layerInstances[0]['__cHei']-0.1
            else: # It failed
                self.lvl = oldlvl
        elif realpos[1] > sur.get_height():
            oldlvl = self.lvl
            self.lvl += ceil(sqrt(len(self.world.ldtk.levels)))
            if self.load_sur():
                pos[1] = 0.1
            else: # It failed
                self.lvl = oldlvl
        
        pos[0] = max(min(pos[0], self.Game.currentLvL.layerInstances[0]['__cWid']), 0)
        pos[1] = max(min(pos[1], self.Game.currentLvL.layerInstances[0]['__cHei']), 0)
        
        realpos = ((pos[0] * self.Game.currentLvL.layerInstances[0]['__gridSize']) * scale,
                   (pos[1] * self.Game.currentLvL.layerInstances[0]['__gridSize']) * scale)
        
        sur = pygame.transform.scale(self.sur, (self.sur.get_width()*scale, self.sur.get_height()*scale))
        
        mw, mh = sze[0]/2, sze[1]/2
        ZC = lambda x: (0 if x < 0 else x) # Zero Check
        diff = ((ZC(mw-realpos[0]) or -ZC(realpos[0]-(sur.get_width()-mw))),
                (ZC(mh-realpos[1]) or -ZC(realpos[1]-(sur.get_height()-mh))))
        win.blit(sur, [
            -realpos[0]+mw-diff[0],
            -realpos[1]+mh-diff[1]
            ])
        playersze = self.Game.currentLvL.layerInstances[0]['__gridSize'] * scale
        pygame.draw.rect(win, (0, 0, 0), (mw-diff[0]-(playersze//2), mh-diff[1]-(playersze//2), playersze, playersze), border_radius=2)
        pygame.draw.rect(win, (255, 255, 255), (mw-diff[0]-(playersze//2), mh-diff[1]-(playersze//2), playersze, playersze), width=5, border_radius=2)
