from math import sqrt, ceil
import pygame
import BlazeSudio.graphics.options as GO

class Player:
    def __init__(self, G, world, Game):
        self.Game = Game
        self.G = G
        self.settings = None
        self.lvl = 0
        self.world = world
        self.load_sur()
        self.pos = [0.1, 0.1]
    
    def load_sur(self):
        if len(self.world.ldtk.levels) <= self.lvl or self.lvl < 0:
            return False
        @self.G.Loading
        def LS(slf):
            self.sur = self.world.get_pygame(self.lvl)
            self.minimap = self.world.gen_minimap(highlights={self.lvl: (255, 50, 50)})
        fin, _ = LS()
        if not fin:
            self.G.Abort()
        return True

    def update(self, events, mPos):
        self.settings = self.Game.settings
        win = self.G.WIN
        sze = self.G.size
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] ^ keys[pygame.K_DOWN]:
            if keys[pygame.K_UP]:
                self.pos[1] -= 0.5
            elif keys[pygame.K_DOWN]:
                self.pos[1] += 0.5
        if keys[pygame.K_RIGHT] ^ keys[pygame.K_LEFT]:
            if keys[pygame.K_RIGHT]:
                self.pos[0] += 0.5
            elif keys[pygame.K_LEFT]:
                self.pos[0] -= 0.5
        
        sur = pygame.transform.scale(self.sur, (self.sur.get_width()*self.settings['scale'], self.sur.get_height()*self.settings['scale']))

        # TODO: replace the changing of the level to work with the ldtk neighbours thing and implement that in world.py
        realpos = ((self.pos[0] * self.world.get_level(self.lvl).layerInstances[0]['__gridSize']) * self.settings['scale'], 
                   (self.pos[1] * self.world.get_level(self.lvl).layerInstances[0]['__gridSize']) * self.settings['scale'])
        if realpos[0] > sur.get_width():
            self.lvl += 1
            if self.load_sur():
                self.pos[0] = 0.1
            else: # It failed
                self.lvl -= 1
        elif realpos[0] < 0:
            self.lvl -= 1
            if self.load_sur():
                self.pos[0] = self.world.get_level(self.lvl).layerInstances[0]['__cWid']-0.1
            else: # It failed
                self.lvl += 1
        if realpos[1] < 0:
            oldlvl = self.lvl
            self.lvl -= ceil(sqrt(len(self.world.ldtk.levels)))
            if self.load_sur():
                self.pos[1] = self.world.get_level(self.lvl).layerInstances[0]['__cHei']-0.1
            else: # It failed
                self.lvl = oldlvl
        elif realpos[1] > sur.get_height():
            oldlvl = self.lvl
            self.lvl += ceil(sqrt(len(self.world.ldtk.levels)))
            if self.load_sur():
                self.pos[1] = 0.1
            else: # It failed
                self.lvl = oldlvl
        
        self.pos[0] = max(min(self.pos[0], self.world.get_level(self.lvl).layerInstances[0]['__cWid']), 0)
        self.pos[1] = max(min(self.pos[1], self.world.get_level(self.lvl).layerInstances[0]['__cHei']), 0)
        
        realpos = ((self.pos[0] * self.world.get_level(self.lvl).layerInstances[0]['__gridSize']) * self.settings['scale'],
                   (self.pos[1] * self.world.get_level(self.lvl).layerInstances[0]['__gridSize']) * self.settings['scale'])
        
        sur = pygame.transform.scale(self.sur, (self.sur.get_width()*self.settings['scale'], self.sur.get_height()*self.settings['scale']))
        
        mw, mh = sze[0]/2, sze[1]/2
        ZC = lambda x: (0 if x < 0 else x) # Zero Check
        diff = ((ZC(mw-realpos[0]) or -ZC(realpos[0]-(sur.get_width()-mw))),
                (ZC(mh-realpos[1]) or -ZC(realpos[1]-(sur.get_height()-mh))))
        win.blit(sur, [
            -realpos[0]+mw-diff[0],
            -realpos[1]+mh-diff[1]
            ])
        win.blit(self.minimap, (0, 0))
        win.blit(GO.FNEW(None, 64).render(f'lvl: {self.lvl}', (0, 0, 0)), (self.minimap.get_width()+20, 0))
        pygame.draw.rect(win, (0, 0, 0), (mw-20-diff[0], mh-20-diff[1], 40, 40), border_radius=2)
        pygame.draw.rect(win, (255, 255, 255), (mw-20-diff[0], mh-20-diff[1], 40, 40), width=5, border_radius=2)
