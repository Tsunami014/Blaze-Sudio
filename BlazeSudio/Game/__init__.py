from BlazeSudio.graphics import Graphic
from BlazeSudio.graphics import options as GO
from BlazeSudio.utils import Player
import BlazeSudio.Game.world as world

__all__ = [
    "world",
    "Game"
]

G = Graphic()

class Game:
    def __init__(self):
        self.world = None
        self.debug = None
        self.settings = {
            "scale": 1
        }
    
    def load_map(self, fpath):
        self.world = world.World(fpath)
    
    def SetSettings(self, **kwargs):
        """
        Sets settings for the world
        
        Settings
        --------
        scale : int, default 1
            The scale of the map
        """
        self.settings.update(kwargs)
    
    @G.CGraphic
    def play(self, event, element=None, aborted=False, debug=False): # Play the game
        """
        Play the game!

        Parameters
        ----------
        debug : bool, optional KWARG ONLY
            Whether to play the game in debug mode or not (avaliable for use in your code via Game.debug), by default False
            In Game.debug, there is a whole buncha cool stuff that will help make your game, like a list of all the entities and their ids, 
            customisable scales to find the right one for your purposes, and more.
        """
        self.debug = debug
        if event == GO.EFIRST:
            player = Player(G, self.world, self)
            RBCORNER = GO.PNEW((0, 1), GO.PRBOTTOM.func, 1, 2)
            G.add_custom(player)
            if debug:
                G.add_empty_space(RBCORNER, 0, -50)
                G.add_text('Scale:', GO.CBLACK, RBCORNER)
                def setScale(e):
                    self.settings['scale'] = e.get()
                G.add_num_input(RBCORNER, start=self.settings['scale'], width=20, callback=setScale)
