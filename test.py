from BlazeSudio.Game import Game

G = Game()
G.load_map("test-files/test1.ldtk")

if __name__ == '__main__':
    G.play(True)
