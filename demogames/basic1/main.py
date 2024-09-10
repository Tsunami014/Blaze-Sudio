from BlazeSudio.Game import Game
from BlazeSudio.collisions import collisions
import BlazeSudio.Game.statics as Ss
import pygame, math

thispth = __file__[:__file__.rindex('/')]

G = Game()
G.load_map(thispth+"/world.ldtk")

class BaseEntity(Ss.BaseEntity):
    pass
    # def __call__(self, keys):
    #     self.handle_accel(keys)
    #     outRect, self.accel = collisions.Rect(self.pos[0]-0.5, self.pos[1]-0.5, 1, 1).handleCollisionsAccel(self.accel, G.currentLvL.layers[1].intgrid.getRects(1), False)
    #     self.pos = [outRect.x, outRect.y]

@G.DefaultSceneLoader
class MainGameScene(Ss.BaseScene):
    def __init__(self, Game, **settings):
        super().__init__(Game, **settings)
        self.entities.append(BaseEntity()) # The Player
        for e in self.currentLvl.entities:
            if e['defUid'] == 107:
                self.entities[0].pos = [e['px'][0] / e['width'], e['px'][1] / e['height']]
                break
    
    def CamPos(self):
        return self.entities[0].pos
    
    def CamDist(self):
        return 8

    def render(self):
        @self.Game.G.Loading
        def LS(slf):
            slf.sur = self.Game.world.get_pygame(0)
        fin, slf = LS()
        if not fin:
            self.Game.G.Abort()
        return slf.sur
    
    """def check_over_level(self, load_sur): # TODO: This
        # TODO: replace the changing of the level to work with the ldtk neighbours thing and implement that in world.py
        if realpos[0] > sur.get_width():
            self.lvl += 1
            if load_sur():
                self.entities[0].pos[0] = 0.1
            else: # It failed
                self.lvl -= 1
        elif realpos[0] < 0:
            self.lvl -= 1
            if load_sur():
                self.entities[0].pos[0] = self.Game.currentLvL.layerInstances[0]['__cWid']-0.1
            else: # It failed
                self.lvl += 1
        if realpos[1] < 0:
            oldlvl = self.lvl
            self.lvl -= math.ceil(math.sqrt(len(self.world.ldtk.levels)))
            if load_sur():
                self.entities[0].pos[1] = self.Game.currentLvL.layerInstances[0]['__cHei']-0.1
            else: # It failed
                self.lvl = oldlvl
        elif realpos[1] > sur.get_height():
            oldlvl = self.lvl
            self.lvl += math.ceil(math.sqrt(len(self.world.ldtk.levels)))
            if load_sur():
                self.entities[0].pos[1] = 0.1
            else: # It failed
                self.lvl = oldlvl"""
    
    def renderUI(self, win, offset, midp, scale):
        playersze = scale
        r = (midp[0]-offset[0]-(playersze//2), midp[1]-offset[1]-(playersze//2), playersze, playersze)
        pygame.draw.rect(win, (0, 0, 0), r, border_radius=2)
        pygame.draw.rect(win, (255, 255, 255), r, width=5, border_radius=2)

G.load_scene(None)

G.play(debug=True)
