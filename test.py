from BlazeSudio.Game import Game
import BlazeSudio.Game.statics as Ss

G = Game()
G.load_map("test-files/world.ldtk")
G.SetSettings(scale=8, gravity=[0, 0.1])

@G.Player
class player(Ss.BasePlayer):
    StartUID = 107

if __name__ == '__main__':
    G.play(debug=True)
