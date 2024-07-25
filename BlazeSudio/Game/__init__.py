from BlazeSudio.graphics import Graphic
from BlazeSudio.graphics import options as GO
from BlazeSudio.utils import Player
import BlazeSudio.Game.world as world
from pyperclip import copy

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
    def play(self, event, element=None, aborted=False, debug=False):
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
        if event == GO.ELOADUI:
            player = Player(G, self.world, self)
            G.add_custom(player)
            
            @G.Graphic
            def help(event, element=None, aborted=False):
                """
                List all the commands!
                """
                if event == GO.ELOADUI:
                    G.add_text('ALL COMMANDS', GO.CBLACK, GO.PCTOP, GO.FTITLE)
                    G.add_text('Press "esc" to go back', GO.CBLACK, GO.PCTOP)
                    newG, e = G.add_Scrollable(GO.PLCENTER, (G.size[0]/3, G.size[0]/2), (G.size[0]/3, G.size[0]))
                    newG2, e = G.add_Scrollable(GO.PRCENTER, (G.size[0]/3, G.size[0]/2), (G.size[0]/3, G.size[0]))
                    rainbow = GO.CRAINBOW()
                    def add_cmd(cmd, txt, cpy):
                        col = next(rainbow)
                        newG.add_text(cmd, col, GO.PCTOP)
                        newG.add_text(txt, col, GO.PCTOP)
                        newG.add_button('Copy command', col, GO.PCTOP, callback=lambda e: copy(cpy))
                    add_cmd('/help ...', 'Get help; a list of all the commands you can use!', '/help')
                    add_cmd('/items ...', 'Go to the items page: to view all the entities and other useful information in the game/level!', '/items')
                    add_cmd('/set <setting> <setTo>', 'Set a setting. See "Settings"', '/set ')
                    add_cmd('/get <setting> ...', 'Gets a setting. See "Settings"', '/get ')
                    newG2.add_text('Settings', GO.CBLACK, GO.PCTOP, GO.FTITLE)
                    newG2.add_text('"scale": the scale of the level', GO.CBLACK, GO.PCTOP)
            
            @G.Graphic
            def items(event, element=None, aborted=False):
                """
                List all the entities and other things in the game and their ids and stuff!
                """
                if event == GO.ELOADUI:
                    TOPLEFT = GO.PNEW((0, 1), GO.PRTOP.func, 0, 0)
                    G.add_button('Copy', GO.CBLACK, TOPLEFT, callback=lambda e: copy('TOP LEFT'))
                    TOPRIGHT = GO.PNEW((0, 1), GO.PRTOP.func, 2, 0)
                    G.add_button('Copy :)', GO.CBLACK, TOPRIGHT, callback=lambda e: copy('TOP RIGHT'))
            
            def tbEnter(txt):
                txt = txt.lower().strip()
                if not txt.startswith('/'):
                    return
                args = txt.split(' ')
                if args[0] == '/set':
                    if len(args) != 3:
                        G.Toast('Incorrect amount of arguments for command "/set"! Expected: 2')
                    else:
                        if args[1] == 'scale':
                            if not args[2].isnumeric():
                                G.Toast('Expected argument 2 of "/set" to be a number, but was not!')
                            else:
                                self.settings['scale'] = int(args[2])
                        else:
                            G.Toast('Invalid setting to set!')
                elif args[0] == '/get':
                    if args[1] == 'scale':
                        G.Toast(f"Scale is {self.settings['scale']}")
                    else:
                        G.Toast('Invalid setting to get!')
                elif args[0] == '/help':
                    help()
                elif args[0] == '/items':
                    items()
                else:
                    G.Toast('Invalid command! for help use /help')
            G.TB.onEnter = tbEnter
