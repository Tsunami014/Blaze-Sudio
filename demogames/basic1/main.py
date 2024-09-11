from BlazeSudio.Game import Game
from BlazeSudio.collisions import collisions
import BlazeSudio.Game.statics as Ss
import pygame

thispth = __file__[:__file__.rindex('/')]

G = Game()
G.load_map(thispth+"/world.ldtk")

class BaseEntity(Ss.BaseEntity):
    def __init__(self):
        super().__init__()
        self.gravity = [0, 0.1]
    
    def __call__(self, evs):
        self.handle_keys()
        self.handle_accel()
        colls = G.currentLvL.layers[1].intgrid.getRects(1)
        for i in colls:
            i.bounciness = 1
        outRect, self.accel = collisions.Rect(self.pos[0]-0.5, self.pos[1]-0.5, 1, 1).handleCollisionsAccel(self.accel, colls, False)
        self.pos = [outRect.x+0.5, outRect.y+0.5]

def isValidLevel(lvl):
    return 0 <= lvl < len(G.world.ldtk.levels)

@G.DefaultSceneLoader
class MainGameScene(Ss.BaseScene):
    def __init__(self, Game, **settings):
        super().__init__(Game, **settings)
        self.sur = None
        self.lvl = settings.get('lvl', 0)
        self.entities.append(BaseEntity()) # The Player
        self.entities[0].pos = [0.1, 0.1]
        if settings.get('UsePlayerStart', False):
            for e in self.currentLvl.entities:
                if e.defUid == 107:
                    self.entities[0].pos = [e.UnscaledPos[0]+0.5, e.UnscaledPos[1]+0.5]
                    break
    
    def CamPos(self):
        return self.entities[0].pos
    
    def CamDist(self):
        return 8

    def render(self):
        if self.sur is not None:
            return self.sur
        @self.Game.G.Loading
        def LS(slf):
            self.sur = self.Game.world.get_pygame(self.lvl)
        fin, _ = LS()
        if not fin:
            self.Game.G.Abort()
        return self.sur
    
    def tick(self, keys):
        super().tick(keys)
        # TODO: Not need the 'self.Game.currentLvL.layerInstances[0]['__gridSize']'
        # TODO: Put player in correct position when changing levels
        for n in self.currentLvl._neighbours:
            if (self.entities[0].pos[0] >= self.currentLvl.width / self.currentLvl.layerInstances[0]['__gridSize'] and n['dir'] == 'e') or \
                (self.entities[0].pos[0] <= 0 and n['dir'] == 'w') or \
                (self.entities[0].pos[1] <= 0 and n['dir'] == 'n') or \
                (self.entities[0].pos[1] >= self.currentLvl.height / self.currentLvl.layerInstances[0]['__gridSize'] and n['dir'] == 's'):
                G.load_scene(lvl=[i.iid for i in self.Game.world.ldtk.levels].index(n['levelIid']))
    
    def renderUI(self, win, offset, midp, scale):
        playersze = scale
        r = (midp[0]-offset[0]-(playersze//2), midp[1]-offset[1]-(playersze//2), playersze, playersze)
        pygame.draw.rect(win, (0, 0, 0), r, border_radius=2)
        pygame.draw.rect(win, (255, 255, 255), r, width=5, border_radius=2)

G.load_scene(UsePlayerStart=True)

G.play(debug=True)
