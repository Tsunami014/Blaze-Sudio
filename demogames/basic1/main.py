from BlazeSudio.Game import Game
from BlazeSudio.collisions import collisions
import BlazeSudio.Game.statics as Ss
import pygame

thispth = __file__[:__file__.rindex('/')]

G = Game()
G.load_map(thispth+"/world.ldtk")

class BaseEntity(Ss.BaseEntity):
    def __init__(self, e):
        super().__init__(e)
        self.accel_amnt = [[0.1, 0.1], [0.05, 0.05]]
        self.gravity = [0, 0.05]
    
    # def __call__(self, evs):
    #     self.handle_keys()
    #     self.handle_accel()
    #     colls = G.currentLvL.layers[1].intgrid.getRects(1)
    #     #for i in colls:
    #     #    i.bounciness = 1
    #     outRect, self.accel = collisions.Rect(self.scaled_pos[0]-0.5, self.scaled_pos[1]-0.5, 1, 1).handleCollisionsAccel(self.accel, colls, False)
    #     self.pos = [outRect.x+0.5, outRect.y+0.5]
    
    @property
    def scaled_pos(self):
        return self.entity.scale_pos(self.pos)

def isValidLevel(lvl):
    return 0 <= lvl < len(G.world.ldtk.levels)

@G.DefaultSceneLoader
class MainGameScene(Ss.BaseScene):
    DefaultEntity = []
    def __init__(self, Game, **settings):
        super().__init__(Game, **settings)
        self.sur = None
        self.CamDist = 8
        self.lvl = settings.get('lvl', 0)
        for e in self.currentLvl.entities:
            if e.defUid == 107:
                self.entities.append(BaseEntity(e)) # The Player
                self.DefaultEntity.append(e)
                self.entities[0].pos = [e.UnscaledPos[0]+0.5, e.UnscaledPos[1]+0.5]
                break
        if self.entities == []:
            if self.DefaultEntity != []:
                self.entities.append(BaseEntity(self.DefaultEntity[-1]))
            else:
                raise Ss.IncorrectLevelError(
                    'Need a player start!'
                )
    
    @property
    def CamPos(self):
        return self.entities[0].scaled_pos

    def render(self):
        if self.sur is not None:
            return self.sur
        self.sur = self.Game.world.get_pygame(self.lvl)
        return self.sur
    
    def tick(self, evs):
        super().tick(evs)
        # TODO: Put player in correct position when changing levels
        playere = self.entities[0]
        for n in self.currentLvl.neighbours:
            if (playere.scaled_pos[0] >= self.currentLvl.sizePx[0] and n['dir'] == 'e') or \
                (playere.scaled_pos[0] <= 0 and n['dir'] == 'w') or \
                (playere.scaled_pos[1] <= 0 and n['dir'] == 'n') or \
                (playere.scaled_pos[1] >= self.currentLvl.sizePx[1] and n['dir'] == 's'):
                G.load_scene(lvl=[i.iid for i in self.Game.world.ldtk.levels].index(n['levelIid']))
    
    def renderUI(self, win, offset, midp, scale):
        playersze = scale
        r = (midp[0]-offset[0]-(playersze//2), midp[1]-offset[1]-(playersze//2), playersze, playersze)
        pygame.draw.rect(win, (0, 0, 0), r, border_radius=2)
        pygame.draw.rect(win, (255, 255, 255), r, width=5, border_radius=2)

G.load_scene(UsePlayerStart=True)

G.play(debug=True)
