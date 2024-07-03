from BlazeSudio.utils import Player
from BlazeSudio.worldGen import World
import BlazeSudio.graphics as graphics

class Game:
    def __init__(self):
        self.G = graphics.Graphic()
        self.world = None
    
    def load_map(self, fpath):
        self.world = World(fpath, make_new=False)
    
    def play(self, debug=False): # Play the game
        player = Player(self.G, self.world)
        @self.G.Graphic
        def game(event, element=None, aborted=False):
            if event == graphics.options.EFIRST:
                self.G.add_custom(player)
        game()
    
    def build(self): # Launch a screen to show all the things you've defined and what you haven't
        pass
