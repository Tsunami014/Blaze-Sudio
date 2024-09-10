from BlazeSudio.Game import Game
from BlazeSudio.collisions import collisions
import BlazeSudio.Game.statics as Ss

thispth = __file__[:__file__.rindex('/')]

G = Game()
G.load_map(thispth+"/world.ldtk")

class BaseEntity(Ss.BaseEntity):
    def __call__(self, keys):
        self.handle_accel(keys)
        outRect, self.accel = collisions.Rect(self.pos[0]-0.5, self.pos[1]-0.5, 1, 1).handleCollisionsAccel(self.accel, G.currentLvL.layers[1].intgrid.getRects(1), False)
        self.pos = [outRect.x, outRect.y]

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

G.load_scene(None)

G.play(debug=True)
