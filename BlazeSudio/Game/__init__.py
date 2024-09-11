from BlazeSudio.graphics import Graphic
from BlazeSudio.graphics import options as GO
from BlazeSudio.Game.player import Player
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
G.Stuff.insert_layer(0).add('Player')

class Game:
    def __init__(self):
        self.G = G
        self.world: world.World = None
        self.debug: bool = None
        self.playing = False
        self.needCreateScene = False

        self.curScene = None
        self.sceneLoader = statics.BaseScene
        self.gameplayer: Player = None # The object which renders the game (like a video player)

        self.scenes = []
        self.cmds = []
        self.sceneLoader = 0
    
    @property
    def currentLvL(self):
        return self.world.get_level(self.curScene.lvl)
    
    @property
    def currentScene(self):
        return self.curScene
    
    def DefaultSceneLoader(self, cls):
        self.sceneLoader = cls
    
    def load_map(self, fpath):
        self.world = world.World(fpath)
    
    def load_scene(self, type=None, **sceneSettings):
        if type is None:
            type = self.sceneLoader
        if self.playing:
            self.curScene = type(self, **sceneSettings)
        else:
            self.curScene = (type, sceneSettings)
        self.needCreateScene = not self.playing
        G.Stuff.clear(['Player', 'TB']) # IGNORE the player and TerminalBar
    
    def AddCommand(self, name, desc, func):
        self.cmds.append([name, desc, func])
    
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
        self.playing = True
        if event == GO.EFIRST:
            self.gameplayer = Player(G, self.world, self)
            if self.needCreateScene:
                self.needCreateScene = False
                self.curScene = self.curScene[0](self, **self.curScene[1])
        elif event == GO.ELOADUI:
            G.add_custom(self.gameplayer, 'Player')
            
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
                        newG.add_text('Built-in commands', GO.CBLACK, GO.PCTOP, GO.FTITLE)
                        def add_cmd(cmd, txt, cpy):
                            col = next(rainbow)
                            newG.add_text(cmd, col, GO.PCTOP, allowed_width=G.size[0]/3-10)
                            newG.add_text(txt, col, GO.PCTOP, allowed_width=G.size[0]/3-10)
                            newG.add_button('Copy command', col, GO.PCTOP, callback=lambda e: copy(cpy))
                        add_cmd('/help ...', 'Get help; a list of all the commands you can use!', '/help')
                        add_cmd('/items ...', 'Go to the items page: to view all the entities and other useful information in the game/level!', '/items')
                        newG2.add_empty_space(GO.PCTOP, 0, 10)
                        newG2.add_text('Game-specific commands', GO.CBLACK, GO.PCTOP, GO.FTITLE)
                        rainbow = GO.CRAINBOW()
                        def add_sett(txt):
                            col = next(rainbow)
                            newG2.add_text(txt, col, GO.PCTOP, allowed_width=G.size[0]/3-10)
                        for name, desc, _ in self.cmds:
                            add_sett(f'"{name}": {desc}')
                
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
                            docsze = 0
                            if e.doc:
                                doc = G.add_text(e.doc, GO.CBLACK, TOPLEFT, GO.FSMALL)
                                docsze = doc.size[0]
                            size = 60
                            scaleby = size / max(e.width, e.height)
                            UITile = pygame.transform.scale(e.get_tile(True), (e.width * scaleby, e.height * scaleby))
                            InGameTile = pygame.transform.scale(e.get_tile(False), (e.width * scaleby, e.height * scaleby))
                            idfp = idf.stackP()
                            ms = max(idf.size[0], docsze) + 10
                            G.add_surface(UITile, GO.PSTATIC(idfp[0] + ms, idfp[1]))
                            G.add_surface(InGameTile, GO.PSTATIC(idfp[0] + ms + size + 10, idfp[1]))
                            def func(e):
                                copy(e.uid)
                                G.Toast(f'Copied "{e.uid}" to clipboard!')
                            G.add_button(f'Copy uid ({e.uid})', next(rainbow), TOPLEFT, font=GO.FSMALL, callback=lambda *args, e=e: func(e))
                            G.add_empty_space(TOPLEFT, 0, 10)
                
                @tb.onEnter
                def tbEnter(txt):
                    txt = txt.lower().strip()
                    cmdNms = [i[0] for i in self.cmds]
                    if not txt.startswith('/'):
                        return
                    args = txt.split(' ')
                    if args[0] == '/help':
                        help()
                    elif args[0] == '/items':
                        items()
                    elif args[0] in cmdNms:
                        self.cmds[cmdNms.index(args[0])][2](*args[1:])
                    else:
                        G.Toast('Invalid command! for help use /help') # TODO: Difflib get_close_matches
        elif event == GO.ETICK:
            pass
