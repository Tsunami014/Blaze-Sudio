from BlazeSudio.Game import Game
from BlazeSudio.collisions import collisions
import BlazeSudio.Game.statics as Ss

thispth = __file__[:__file__.rindex('/')]

G = Game()
G.load_map(thispth+"/world.ldtk")
G.SetSettings(scale=8, gravity=[0, 0.1])

@G.Collision
class Collisions(Ss.BaseCollisions):
    def __call__(self, pos, accel, entity):
        ret = collisions.Rect(pos[0]-0.5, pos[1]-0.5, 1, 1).handleCollisionsAccel(accel, G.currentLvL.layers[1].intgrid.getRects(1), False)
        return (ret[0][0][0]+0.5, ret[0][0][1]+0.5), ret[1]

@G.Player
class player(Ss.BasePlayer):
    StartUID = 107

G.play(debug=True)
