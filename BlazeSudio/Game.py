from BlazeSudio.graphics import Graphic
from BlazeSudio.graphics import options as GO
from BlazeSudio.utils import Player
from BlazeSudio.worldGen import World

G = Graphic()

class Game:
    def __init__(self):
        self.world = None
    
    def load_map(self, fpath):
        self.world = World(fpath, make_new=False)
    
    @G.CGraphic
    def play(self, event, element=None, aborted=False, debug=False): # Play the game
        if event == GO.EFIRST:
            player = Player(G, self.world)
            self.G.add_custom(player)
    
    @G.CGraphic
    def build(self, event, element=None, aborted=False): # Launch a screen to show all the things you've defined and what you haven't
        if event == GO.ELOADUI:
            G.Clear()
            if self.world is None:
                G.add_text("No world loaded!", GO.CBLACK, GO.PCCENTER)
            else:
                G.add_text("Loaded world '%s'!"%self.world.name, GO.CBLACK, GO.PCCENTER)
