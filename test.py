from BlazeSudio.Game import Game
import BlazeSudio.Game.statics as Ss

G = Game()
G.load_map("test-files/world.ldtk")
G.SetSettings(scale=8, gravity=[0, 0.1])

@G.Collision
class Collisions(Ss.BaseCollisions):
    def __call__(self, pos, entity):
        # if entity == "Player":
        return not all([i != 1 for i in G.currentLvL.layers[1].intgrid.getAllHits([pos[0], pos[1]], [1, 1])])
        #return not all([i != 1 for i in G.currentLvL.layers[1].intgrid.getAllHits([pos[0]+0.375, pos[1]+0.375], [0.75, 0.75])])

@G.Player
class player(Ss.BasePlayer):
    StartUID = 107

if __name__ == '__main__':
    G.play(debug=True)
