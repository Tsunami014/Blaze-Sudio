from BlazeSudio.Game import Game
from BlazeSudio.collisions import collisions
import BlazeSudio.Game.statics as Ss
import pygame

thispth = __file__[:__file__.rindex('/')]

G = Game()
G.load_map(thispth+"/levels.ldtk")

class BaseEntity(Ss.BaseEntity):
    pass
    #def __call__(self, keys):
    #    self.handle_accel(keys)
    #    outRect, self.accel = collisions.Rect(self.pos[0]-0.5, self.pos[1]-0.5, 1, 1).handleCollisionsAccel(self.accel, G.currentLvL.layers[1].intgrid.getRects(1), False)
    #    self.pos = [outRect.x, outRect.y]

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
        lvl = self.currentLvl
        sur = pygame.Surface((lvl.pxWid, lvl.pxHei))
        for e in lvl.entities:
            typs = ['Collisions', 'GravityFields']
            col = (255, 255, 255) if e['layerId'] not in typs else [(255, 50, 50), (10, 255, 50)][typs.index(e['layerId'])]
            if e['__identifier'] == 'CircleRegion':
                pygame.draw.circle(sur, col, (e['__worldX']+e['width']//2, e['__worldY']+e['height']//2), e['width']) # TODO: Elipses
            elif e['__identifier'] == 'RectRegion':
                pygame.draw.rect(sur, col, (e['__worldX'], e['__worldY'], e['width'], e['height']))
        return sur
G.load_scene(None)

G.play(debug=True)
