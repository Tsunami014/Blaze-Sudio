from BlazeSudio.graphics import Graphic
from BlazeSudio.graphics import options as GO
from BlazeSudio.utils import Player
from pyperclip import copy

import pygame.transform

import BlazeSudio.Game.world as world
import BlazeSudio.Game.statics as statics


__all__ = [
    "Game",
    "world",
    "statics"
]

G = Graphic()


_settings = {
    # Name: (type, type explanation, default, explanation)
    "scale": (statics.Number, "Number", 1, "the scale of the level"),
    "gravity": (statics.Iterable, "list[int,int]", [0, 0], "the gravity of the player, x and y")
}

class Game:
    def __init__(self):
        self.world: world.World = None
        self.debug: bool = None
        self._player: statics.BasePlayer = None # The player character in the game
        self._gameplayer: Player = None # The object which renders the game (like a video player)
        self._scenes = []
        self._defaultScene = 0
        self.settings = {
            i: i[2] for i in _settings
        }
        self._onticks = []
        self._collisionfunc = None
    
    @property
    def currentLvL(self):
        return self._gameplayer.currentLvL
    
    def Collision(self, func):
        self._collisionfunc = func
        return func
    
    def Scene(self, func, default=False):
        pass
    
    def Player(self, cls):
        self._player = cls()
        return cls
    
    def load_map(self, fpath):
        self.world = world.World(fpath)
    
    def SetSettings(self, **kwargs):
        """
        Sets settings for the world
        
        Settings
        --------
        scale : int, default 1
            The scale of the map
        gravity : list[int,int], default [0, 0]
            The gravity of the player, in x, y
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
        if event == GO.EFIRST:
            self._gameplayer = Player(G, self.world, self)
            if self._player is not None and self._player.StartUID is not None:
                for e in self.world.get_level(self._gameplayer.lvl).entities:
                    if e['defUid'] == self._player.StartUID:
                        self._gameplayer.pos = [e['px'][0] / e['width'], e['px'][1] / e['height']]
                        break
        elif event == GO.ELOADUI:
            G.add_custom(self._gameplayer)
            
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
                        for i in _settings:
                            it = _settings[i]
                            add_sett(f'"{i}" ({it[1]}): {it[3]}, default: {it[2]}')
                
                @G.Graphic
                def items(event, element=None, aborted=False):
                    """
                    List all the entities and other things in the game and their ids and stuff!
                    """
                    if event == GO.ELOADUI:
                        G.Clear()
                        G.add_text("""
Please note:
1. If you used the internal icons it will appear blurry and without transparency. You're lucky I even provided you with THAT. PLEASE do not use them in your final game; the creator SPECIFICALLY said not to. I accept NO responsibility for you using this WHATSOEVER.
2. The first image is the editor icon and the second is the actual image that will be in the game.
""", GO.CBLACK, GO.PCTOP, allowed_width=500)
                        TOPLEFT = GO.PNEW((0, 1), GO.PLTOP.func, 0, 0)
                        G.add_text('All entities', GO.CBLACK, TOPLEFT, GO.FTITLE)
                        TOPRIGHT = GO.PNEW((0, 1), GO.PRTOP.func, 2, 0)
                        G.add_text('Entities in this level', GO.CBLACK, TOPRIGHT, GO.FTITLE)
                        rainbow = GO.CRAINBOW()
                        for e in self.world.ldtk.entities:
                            idf = G.add_text(e.identifier, GO.CBLACK, TOPLEFT)
                            doc = G.add_text(e.doc, GO.CBLACK, TOPLEFT, GO.FSMALL)
                            size = 60
                            scaleby = size / max(e.width, e.height)
                            UITile = pygame.transform.scale(e.get_tile(True), (e.width * scaleby, e.height * scaleby))
                            InGameTile = pygame.transform.scale(e.get_tile(False), (e.width * scaleby, e.height * scaleby))
                            idfp = idf.stackP()
                            ms = max(idf.size[0], doc.size[0]) + 10
                            G.add_surface(UITile, GO.PSTATIC(idfp[0] + ms, idfp[1]))
                            G.add_surface(InGameTile, GO.PSTATIC(idfp[0] + ms + size + 10, idfp[1]))
                            G.add_button(f'Copy uid ({e.uid})', next(rainbow), TOPLEFT, font=GO.FSMALL, callback=copy(e.uid))
                            G.add_empty_space(TOPLEFT, 0, 10)
                
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
                                    out = eval(args[2])
                                    assert isinstance(out, _settings[args[1]][0])
                                    self.settings[args[1]] = out
                                except:
                                    G.Toast(f'Expected argument 2 of "/set" to be a {_settings[args[1]][1]}, but was not!')
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
                        G.Toast('Invalid command! for help use /help') # TODO: Difflib get_close_matches
        elif event == GO.ETICK:
            self._gameplayer.gravity = self.settings['gravity']
            for i in self._onticks:
                i()
