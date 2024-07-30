from math import sqrt, ceil
import pygame
import BlazeSudio.graphics.options as GO
import BlazeSudio.Game.statics as statics

class Player:
    def __init__(self, G, world, Game):
        self.Game = Game
        self.G = G
        self.settings = None
        self.lvl = 0
        self.world = world
        self.load_sur()
        self.pos = [0.1, 0.1]
        self.accel = [0, 0]
        #                   Accel,      decel
        self.accel_amnt = [[0.2, 0.2], [0.25, 0.25]]
        self.max_accel = [0.7, 0.7]
        self.gravity = [0, 0]
    
    @property
    def currentLvL(self):
        return self.world.get_level(self.lvl)
    
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
                self.accel[1] -= self.accel_amnt[0][1]
            elif keys[pygame.K_DOWN]:
                self.accel[1] += self.accel_amnt[0][1]
        else:
            if self.accel[1] < -self.accel_amnt[1][1]:
                self.accel[1] += self.accel_amnt[1][1]
            elif self.accel[1] > self.accel_amnt[1][1]:
                self.accel[1] -= self.accel_amnt[1][1]
            else:
                self.accel[1] = 0
        
        if keys[pygame.K_RIGHT] ^ keys[pygame.K_LEFT]:
            if keys[pygame.K_RIGHT]:
                self.accel[0] += self.accel_amnt[0][0]
            elif keys[pygame.K_LEFT]:
                self.accel[0] -= self.accel_amnt[0][0]
        else:
            if self.accel[0] < -self.accel_amnt[1][0]:
                self.accel[0] += self.accel_amnt[1][0]
            elif self.accel[0] > self.accel_amnt[1][0]:
                self.accel[0] -= self.accel_amnt[1][0]
            else:
                self.accel[0] = 0
        
        self.accel = [round(min(max(self.accel[0]+self.gravity[0], -self.max_accel[0]), self.max_accel[0]), 3), round(min(max(self.accel[1]+self.gravity[1], -self.max_accel[1]), self.max_accel[1]), 3)]
        
        if not self.Game._collisions([self.pos[0] + self.accel[0], self.pos[1]], "Player"):
            self.pos = [self.pos[0] + self.accel[0], self.pos[1]]
        else:
            tries = self.Game._collisions.num_checks(self.pos[0] + self.accel[0], "Player")
            if tries > 1:
                for i in range(tries-1, -1, -1):
                    if not self.Game._collisions([self.pos[0] + self.accel[0]*(i/tries), self.pos[1]], "Player"):
                        self.pos = [self.pos[0] + self.accel[0]*(i/tries), self.pos[1]]
                        break
            self.accel[0] = 0
            #self.pos, self.accel[0] = self.Game._collisions.fine_check(self.pos, self.accel[0], True, "Player")
        
        if not self.Game._collisions([self.pos[0], self.pos[1] + self.accel[1]], "Player"):
            self.pos = [self.pos[0], self.pos[1] + self.accel[1]]
        else:
            tries = self.Game._collisions.num_checks(self.pos[1] + self.accel[1], "Player")
            if tries > 1:
                for i in range(tries-1, -1, -1):
                    if not self.Game._collisions([self.pos[0], self.pos[1] + self.accel[1]*(i/tries)], "Player"):
                        self.pos = [self.pos[0], self.pos[1] + self.accel[1]*(i/tries)]
                        break
            self.accel[0] = 0
            #self.pos, self.accel[1] = self.Game._collisions.fine_check(self.pos, self.accel[1], False, "Player")
        
        sur = pygame.transform.scale(self.sur, (self.sur.get_width()*self.settings['scale'], self.sur.get_height()*self.settings['scale']))

        # TODO: replace the changing of the level to work with the ldtk neighbours thing and implement that in world.py
        realpos = ((self.pos[0] * self.currentLvL.layerInstances[0]['__gridSize']) * self.settings['scale'], 
                   (self.pos[1] * self.currentLvL.layerInstances[0]['__gridSize']) * self.settings['scale'])
        if realpos[0] > sur.get_width():
            self.lvl += 1
            if self.load_sur():
                self.pos[0] = 0.1
            else: # It failed
                self.lvl -= 1
        elif realpos[0] < 0:
            self.lvl -= 1
            if self.load_sur():
                self.pos[0] = self.currentLvL.layerInstances[0]['__cWid']-0.1
            else: # It failed
                self.lvl += 1
        if realpos[1] < 0:
            oldlvl = self.lvl
            self.lvl -= ceil(sqrt(len(self.world.ldtk.levels)))
            if self.load_sur():
                self.pos[1] = self.currentLvL.layerInstances[0]['__cHei']-0.1
            else: # It failed
                self.lvl = oldlvl
        elif realpos[1] > sur.get_height():
            oldlvl = self.lvl
            self.lvl += ceil(sqrt(len(self.world.ldtk.levels)))
            if self.load_sur():
                self.pos[1] = 0.1
            else: # It failed
                self.lvl = oldlvl
        
        self.pos[0] = max(min(self.pos[0], self.currentLvL.layerInstances[0]['__cWid']), 0)
        self.pos[1] = max(min(self.pos[1], self.currentLvL.layerInstances[0]['__cHei']), 0)
        
        realpos = ((self.pos[0] * self.currentLvL.layerInstances[0]['__gridSize']) * self.settings['scale'],
                   (self.pos[1] * self.currentLvL.layerInstances[0]['__gridSize']) * self.settings['scale'])
        
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
        playersze = self.currentLvL.layerInstances[0]['__gridSize'] * self.settings['scale']
        pygame.draw.rect(win, (0, 0, 0), (mw-diff[0]-(playersze//2), mh-diff[1]-(playersze//2), playersze, playersze), border_radius=2)
        pygame.draw.rect(win, (255, 255, 255), (mw-diff[0]-(playersze//2), mh-diff[1]-(playersze//2), playersze, playersze), width=5, border_radius=2)
