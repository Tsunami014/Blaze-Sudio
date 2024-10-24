from BlazeSudio.graphics import Graphic, GUI
from BlazeSudio.graphics import options as GO
from BlazeSudio.graphics.GUI.base import ReturnState
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
G.Stuff.insert_layer().add_many(['TB', 'OverlayGUI']) # FIXME

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
    def UILayer(self):
        return G.layers[1]
    
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
        keeps = (G['Player'], G['TB'])
        G.Clear()
        G['Player'], G['TB'] = keeps
        if self.playing:
            self.curScene = type(self, **sceneSettings)
        else:
            self.curScene = (type, sceneSettings)
        self.needCreateScene = not self.playing

        return ReturnState.STOP
    
    def AddCommand(self, name, desc, func):
        self.cmds.append([name, desc, func])
    
    @G.Screen
    def play(event, self, element=None, aborted=False, debug=False):
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
            G['Player'].append(self.gameplayer)
            
            if debug:
                tb = GUI.TerminalBar(G)
                G['TB'].append(tb)
                
                @G.Screen
                def help(event, element=None, aborted=False):
                    """
                    List all the commands!
                    """
                    if event == GO.ELOADUI:
                        G.Clear()
                        G['OverlayGUI'].append(GUI.Text(G, GO.PCTOP, 'Press "esc" to go back'))
                        newG = GUI.ScrollableFrame(G, GO.PLCENTER, (G.size[0]/3, G.size[1]/2), (G.size[0]/3, 0))
                        newG2 = GUI.ScrollableFrame(G, GO.PRCENTER, (G.size[0]/3, G.size[1]/2), (G.size[0]/3, 0))
                        G['OverlayGUI'].extend([newG, newG2])

                        newG.layers[0].add('Alls')
                        rainbow = GO.CRAINBOW()

                        def add_cmd(cmd, txt, cpy):
                            col = next(rainbow)
                            return [
                                GUI.Text(newG, GO.PCTOP, cmd, col, allowed_width=G.size[0]/3-10),
                                GUI.Text(newG, GO.PCTOP, txt, col, allowed_width=G.size[0]/3-10),
                                GUI.Button(newG, GO.PCTOP, col, 'Copy command', func=lambda e: copy(cpy))
                            ]
                        
                        newG['Alls'].extend([
                            GUI.Empty(newG, GO.PCTOP, (0, 10)),
                            GUI.Text(newG, GO.PCTOP, 'Built-in commands', font=GO.FTITLE)
                        ] + [
                            *add_cmd('/help ...', 'Get help; a list of all the commands you can use!', '/help'),
                            *add_cmd('/items ...', 'Go to the items page: to view all the entities and other useful information in the game/level!', '/items')
                        ])

                        newG2.layers[0].add('Alls')
                        rainbow = GO.CRAINBOW()

                        def add_sett(txt):
                            col = next(rainbow)
                            return GUI.Text(newG2, GO.PCTOP, txt, col, allowed_width=G.size[0]/3-10)
                        
                        newG2['Alls'].extend([
                            GUI.Empty(G, GO.PCTOP, (0, 10)),
                            GUI.Text(G, GO.PCTOP, 'Game-specific commands', font=GO.FTITLE)
                        ] + [
                            add_sett(f'"{i[0]}": {i[1]}') for i in self.cmds
                        ])
                        
                        newG.sizeOfScreen = (G.size[0]/3, max(G.size[1]/2, sum([i.size[1] for i in newG.getAllElms()])))
                        newG2.sizeOfScreen = (G.size[0]/3, max(G.size[1]/2, sum([i.size[1] for i in newG2.getAllElms()])))
                
                @G.Screen
                def items(event, element=None, aborted=False):
                    """
                    List all the entities and other things in the game and their ids and stuff!
                    """
                    if event == GO.ELOADUI:
                        G.Clear()
                        G['OverlayGUI'].append(GUI.Text(G, GO.PCTOP, """
Please note: If you used the internal icons it will appear blurry and without transparency. You're lucky I even provided you with THAT. PLEASE do not use them in your final game; the creator SPECIFICALLY said not to. I accept NO responsibility for you using this WHATSOEVER.
""", allowed_width=500))
                        
                        TOPLEFT = GO.PNEW((0, 0), (0, 1), (False, False))
                        G['OverlayGUI'].append(GUI.Text(G, TOPLEFT, 'All entities', font=GO.FTITLE))
                        scr = GUI.ScrollableFrame(G, GO.PLCENTER, (G.size[0]/2-260, G.size[1]/3*2), (G.size[0]/2, 0))
                        G['OverlayGUI'].append(scr)
                        scr.layers[0].add('Alls')

                        rainbow = GO.CRAINBOW()
                        def func(e):
                            copy(e['uid'])
                            G.Toast(f'Copied "{e['uid']}" to clipboard!')
                        for e in self.world.ldtk.defs['entities']:
                            idf = GUI.Text(scr, TOPLEFT, e['identifier'])
                            scr['Alls'].append(idf)
                            docsze = 0
                            if e['doc']:
                                doc = GUI.Text(scr, TOPLEFT, e['doc'], font=GO.FSMALL)
                                scr['Alls'].append(doc)
                                docsze = doc.size[0]
                            size = 60
                            scaleby = size / max(e['width'], e['height'])
                            if e['renderMode'] == 'Tile':
                                UITile = pygame.transform.scale(self.world.ldtk.tilesets[e['tilesetId']].subsurface(
                                                                    e['tileRect']['x'],
                                                                    e['tileRect']['y'],
                                                                    e['tileRect']['w'],
                                                                    e['tileRect']['h']
                                                                ), (e['width'] * scaleby, e['height'] * scaleby))
                            else:
                                UITile = pygame.Surface((e['width'] * scaleby, e['height'] * scaleby), pygame.SRCALPHA)
                                if e['renderMode'] == 'Rectangle':
                                    pygame.draw.rect(UITile, pygame.Color(e['color']), (0, 0, *UITile.get_size()), border_radius=8)
                                elif e['renderMode'] == 'Ellipse':
                                    pygame.draw.ellipse(UITile, pygame.Color(e['color']), (0, 0, e['width'] * scaleby, e['height'] * scaleby))
                                elif e['renderMode'] == 'Cross':
                                    pygame.draw.line(UITile, pygame.Color(e['color']), (0, 0), (e['width'] * scaleby, e['height'] * scaleby), 2)
                                    pygame.draw.line(UITile, pygame.Color(e['color']), (e['width'] * scaleby, 0), (0, e['height'] * scaleby), 2)
                                else:
                                    UITile.fill((0, 0, 0))
                                    UITile.fill(pygame.Color('purple'), (0, 0, (e['width'] * scaleby) // 2, (e['height'] * scaleby)//2))
                                    UITile.fill(pygame.Color('purple'), ((e['width'] * scaleby) // 2, (e['height'] * scaleby)//2, (e['width'] * scaleby) // 2, (e['height'] * scaleby)//2))
                            
                            idfp = idf.stackP()
                            ms = max(idf.size[0], docsze) + 10
                            scr['Alls'].extend([
                                GUI.Static(scr, GO.PSTATIC(idfp[0] + ms, idfp[1]), UITile),
                                GUI.Button(scr, GO.PSTATIC(idfp[0] + ms + size + 10, idfp[1]), next(rainbow), 'Copy uid (%i)'%e['uid'], func=lambda *args, e=e: func(e)),
                                GUI.Empty(scr, TOPLEFT, (0, e['height'] * scaleby)),
                            ])
                        
                        scr.sizeOfScreen = (G.size[0]/2-260, max(G.size[1]/2, sum([i.size[1] for i in scr.getAllElms()])))
                        
                        TOPRIGHT = GO.PNEW((1, 0), (0, 1), (False, False))
                        G['OverlayGUI'].append(GUI.Text(G, TOPRIGHT, 'Entities in this level', font=GO.FTITLE))
                        # TODO
                
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
                        G['OverlayGUI'].append(GUI.Toast(G, 'Invalid command! for help use /help', GO.CRED)) # TODO: Difflib get_close_matches
        elif event == GO.ETICK:
            pass
