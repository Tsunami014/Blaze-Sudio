from BlazeSudio.Game import Game

G = Game()
G.load_map("test-files/world.ldtk")
G.SetSettings(scale=2000)

if __name__ == '__main__':
    G.play(debug=True)
