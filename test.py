from BlazeSudio.Game import Game
import BlazeSudio.Game.statics as Ss

G = Game()
G.load_map("test-files/world.ldtk")
G.SetSettings(scale=8, gravity=[0, 0.1])

@G.Collision
class Collisions(Ss.BaseCollisions):
    def __call__(self, pos, movement, rect, entity):
        rect.handle_collisions(G.currentLvL.layers[1].intgrid.getRects(1), movement)
        return rect.realPos

@G.Player
class player(Ss.BasePlayer):
    StartUID = 107

if __name__ == '__main__':
    G.play(debug=True)
