from math import sqrt, ceil
import pygame

class Player:
    def __init__(self, world, Loading, quitfunc):
        self.lvl = 0
        self.world = world
        self.Loading = Loading
        self.quitfunc = quitfunc
        self.load_sur()
        self.pos = [self.sur.get_width()/2, self.sur.get_height()/2]
    
    def load_sur(self):
        if len(self.world.ldtk.levels) <= self.lvl or self.lvl < 0:
            return False
        @self.Loading
        def LS(slf):
            self.sur = self.world.get_pygame(self.lvl)
            self.minimap = self.world.gen_minimap(highlights={self.lvl: (255, 50, 50)})
        fin, _ = LS()
        if not fin: self.quitfunc()
        return True

    def execute(self, win):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] ^ keys[pygame.K_DOWN]:
            if keys[pygame.K_UP]:
                self.pos[1] -= 10
            elif keys[pygame.K_DOWN]:
                self.pos[1] += 10
        if keys[pygame.K_RIGHT] ^ keys[pygame.K_LEFT]:
            if keys[pygame.K_RIGHT]:
                self.pos[0] += 10
            elif keys[pygame.K_LEFT]:
                self.pos[0] -= 10

        # TODO: replace the changing of the level to work with the ldtk neighbours thing and implement that in world.py
        if self.pos[0] > self.sur.get_width():
            self.lvl += 1
            if self.load_sur():
                self.pos[0] = 10
            else: # It failed
                self.lvl -= 1
        elif self.pos[0] < 0:
            self.lvl -= 1
            if self.load_sur():
                self.pos[0] = self.sur.get_width()-10
            else: # It failed
                self.lvl += 1
        if self.pos[1] < 0:
            oldlvl = self.lvl
            self.lvl -= ceil(sqrt(len(self.world.ldtk.levels)))
            if self.load_sur():
                self.pos[1] = self.sur.get_height()-10
            else: # It failed
                self.lvl = oldlvl
        elif self.pos[1] > self.sur.get_height():
            oldlvl = self.lvl
            self.lvl += ceil(sqrt(len(self.world.ldtk.levels)))
            if self.load_sur():
                self.pos[1] = 10
            else: # It failed
                self.lvl = oldlvl
        
        # This stays here because if you cannot change levels you must be constraint to the current one
        self.pos[0] = max(min(self.pos[0], self.sur.get_width()), 0)
        self.pos[1] = max(min(self.pos[1], self.sur.get_height()), 0)
        mw, mh = win.get_width()/2, win.get_height()/2
        ZC = lambda x: (0 if x < 0 else x) # Zero Check
        diff = ((ZC(mw-self.pos[0]) or -ZC(self.pos[0]-(self.sur.get_width()-mw))),
                (ZC(mh-self.pos[1]) or -ZC(self.pos[1]-(self.sur.get_height()-mh))))
        win.blit(self.sur, [
            -self.pos[0]+mw-diff[0],
            -self.pos[1]+mh-diff[1]
            ])
        win.blit(self.minimap, (0, 0))
        win.blit(pygame.font.SysFont('', 64).render(f'lvl: {self.lvl}', 1, (0, 0, 0)), (self.minimap.get_width()+20, 0))
        pygame.draw.rect(win, (0, 0, 0), (mw-20-diff[0], mh-20-diff[1], 40, 40), border_radius=2)
