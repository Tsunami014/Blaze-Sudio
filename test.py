from BlazeSudio.Game import Game
from BlazeSudio.utils import collisions
import BlazeSudio.Game.statics as Ss

G = Game()
G.load_map("test-files/world.ldtk")
G.SetSettings(scale=8, gravity=[0, 0.1])

@G.Collision
class Collisions(Ss.BaseCollisions):
    def __call__(self, pos, accel, entity):
        return collisions.handleCollisionsAccel(pos, accel, G.currentLvL.layers[1].intgrid.getRects(1))

@G.Player
class player(Ss.BasePlayer):
    StartUID = 107

if __name__ == '__main__':
    G.play(debug=True)
