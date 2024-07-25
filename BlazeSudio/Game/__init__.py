from BlazeSudio.graphics import Graphic
from BlazeSudio.graphics import options as GO
from BlazeSudio.utils import Player
from pyperclip import copy

import BlazeSudio.Game.world as world
import BlazeSudio.Game.statics as statics


__all__ = [
    "Game",
    "world",
    "statics"
]

G = Graphic()

_types = {
    "scale": statics.Number,
    "gravity": statics.Iterable
}

class Game:
    def __init__(self):
        self.world = None
        self.debug = None
        self.settings = {
            "scale": 1,
            "gravity": [0, -1]
        }
        self._onticks = []
    
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
    
    def ontick(self, func):
        """
        Add a function to be called every tick
        
        Parameters
        ----------
        func : function
            The function to be called
        """
        self._onticks.append(func)
    
    @G.CGraphic
    def play(self, event, element=None, aborted=False, debug=False):
        """
        Play the game!

        Parameters
        ----------
        debug : bool, optional KWARG ONLY
            Whether to play the game in debug mode or not (avaliable for use in your code via Game.debug), by default False
            In Game.debug, there is a whole buncha cool stuff that will help make your game, like a list of all the entities and their ids, 
            customisable scales to find the right one for your purposes, and more; all avaliable via the terminalbar.
        """
        self.debug = debug
        if event == GO.ELOADUI:
            player = Player(G, self.world, self)
            G.add_custom(player)
            
            if debug:
                tb = G.add_TerminalBar()
                
                @G.Graphic
                def help(event, element=None, aborted=False):
                    """
                    List all the commands!
                    """
                    if event == GO.ELOADUI:
                        G.Clear()
                        G.add_text('Press "esc" to go back', GO.CBLACK, GO.PCTOP)
                        newG, e = G.add_Scrollable(GO.PLCENTER, (G.size[0]/3, G.size[0]/2), (G.size[0]/3, G.size[0]))
                        newG2, e = G.add_Scrollable(GO.PRCENTER, (G.size[0]/3, G.size[0]/2), (G.size[0]/3, G.size[0]))
                        rainbow = GO.CRAINBOW()
                        newG.add_empty_space(GO.PCTOP, 0, 10)
                        newG.add_text('ALL COMMANDS', GO.CBLACK, GO.PCTOP, GO.FTITLE)
                        def add_cmd(cmd, txt, cpy):
                            col = next(rainbow)
                            newG.add_text(cmd, col, GO.PCTOP, allowed_width=G.size[0]/3-10)
                            newG.add_text(txt, col, GO.PCTOP, allowed_width=G.size[0]/3-10)
                            newG.add_button('Copy command', col, GO.PCTOP, callback=lambda e: copy(cpy))
                        add_cmd('/help ...', 'Get help; a list of all the commands you can use!', '/help')
                        add_cmd('/items ...', 'Go to the items page: to view all the entities and other useful information in the game/level!', '/items')
                        add_cmd('/set <setting> <setTo>', 'Set a setting. See "Settings"', '/set ')
                        add_cmd('/get <setting> ...', 'Gets a setting. See "Settings"', '/get ')
                        newG2.add_empty_space(GO.PCTOP, 0, 10)
                        newG2.add_text('Settings', GO.CBLACK, GO.PCTOP, GO.FTITLE)
                        def add_sett(txt):
                            newG2.add_text(txt, GO.CBLACK, GO.PCTOP, allowed_width=G.size[0]/3-10)
                        add_sett('"scale" (number): the scale of the level')
                        add_sett('"gravity" (tuple[int,int]): the gravity of the player, x and y')
                
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
                
                @tb.onEnter
                def tbEnter(txt):
                    txt = txt.lower().strip()
                    if not txt.startswith('/'):
                        return
                    args = txt.split(' ')
                    if args[0] == '/set':
                        if len(args) != 3:
                            G.Toast('Incorrect amount of arguments for command "/set"! Expected: 2')
                        else:
                            if args[1] in self.settings:
                                try:
                                    out = eval(args[1])
                                    assert isinstance(out, _types[args[1]])
                                    self.settings[args[1]] = out
                                except:
                                    G.Toast(f'Expected argument 2 of "/set" to be a {str(_types[args[1]])}, but was not!')
                            else:
                                G.Toast('Invalid setting to set!')
                    elif args[0] == '/get':
                        if args[1] in self.settings:
                            G.Toast(f"{args[1]} is {self.settings[args[1]]}")
                        else:
                            G.Toast('Invalid setting to get!')
                    elif args[0] == '/help':
                        help()
                    elif args[0] == '/items':
                        items()
                    else:
                        G.Toast('Invalid command! for help use /help')
        elif event == GO.ETICK:
            for i in self._onticks:
                i()
