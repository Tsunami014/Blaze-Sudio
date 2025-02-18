from BlazeSudio.graphics import Screen, RunInstantly, GUI
from BlazeSudio.graphics import options as GO
from BlazeSudio.graphics.base import ReturnState
from BlazeSudio.Game.player import Player
from pyperclip import copy

import pygame.transform
import inspect

import BlazeSudio.Game.world as world
import BlazeSudio.Game.statics as statics


__all__ = [
    "Game",
    "world",
    "statics"
]

class Game(Screen):
    def __init__(self):
        self.world: world.World = None
        self.isdebug: bool = False
        self.playing = False
        self.needCreateScene = False

        self.curScene = None
        self.sceneLoader = statics.BaseScene
        self.gameplayer: Player = None # The object which renders the game (like a video player)

        self.scenes = []
        self.cmds = []
        self.sceneLoader = 0

        super().__init__()
    
    @property
    def UILayer(self):
        """
        The layer for UI, but if you want a more advanced UI (multiple layers, groups or smthn fancy) just make your own `Screen`; much easier and better.
        """
        return self['Customs']
    
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
        self.Clear('Main')
        if self.playing:
            self.curScene = type(self, **sceneSettings)
        else:
            self.curScene = (type, sceneSettings)
        self.needCreateScene = not self.playing

        return ReturnState.STOP
    
    def AddCommand(self, name, desc, func):
        self.cmds.append([name, desc, func])

    def debug(self):
        """
        Debug the game!!

        (avaliable for querying in your code via `Game.isdebug`)

        In Game.debug, there is a whole buncha cool stuff that will help make your game, like a list of all the entities and their ids, 
        customisable scales to find the right one for your purposes, and more; all avaliable via the terminalbar.
        """
        self.isdebug = True
        self()
    
    def _LoadUI(self):
        self.layers[0].add_many(['Main', 'Toasts'])
        self.insert_layer().add('Customs')

        self['Main'].append(self.gameplayer)
        
        if self.isdebug:
            self._LoadDebugUI()
    
    def _LoadDebugUI(gameself):
        tb = GUI.DebugTerminal(gameself)
        gameself['Main'].append(tb)

        for i in gameself.cmds:
            if inspect.ismethod(i[2]):
                i[2].__func__.__doc__ = i[1]
            else:
                i[2].__doc__ = i[1]
            tb.addCmd(i[0], i[2])
        
        class help(Screen, RunInstantly):
            """
            /help ... : List all the commands!
            """
            def __init__(self, *args):
                super().__init__()
            
            def _LoadUI(self):
                self.layers[0].add('OverlayGUI')
                self['OverlayGUI'].append(GUI.Text(self, GO.PCTOP, 'Press "esc" to go back'))
                newG = GUI.ScrollableFrame(self, GO.PLCENTER, (self.size[0]/3, self.size[1]/2), (self.size[0]/3, 0))
                newG2 = GUI.ScrollableFrame(self, GO.PRCENTER, (self.size[0]/3, self.size[1]/2), (self.size[0]/3, 0))
                self['OverlayGUI'].extend([newG, newG2])

                newG.layers[0].add('Alls')
                rainbow = GO.CRAINBOW()

                def add_cmd(cmd, txt, cpy):
                    col = next(rainbow)
                    return [
                        GUI.Text(newG, GO.PCTOP, cmd, col, allowed_width=self.size[0]/3-10),
                        GUI.Text(newG, GO.PCTOP, txt, col, allowed_width=self.size[0]/3-10),
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
                    return GUI.Text(newG2, GO.PCTOP, txt, col, allowed_width=self.size[0]/3-10)
                
                newG2['Alls'].extend([
                    GUI.Empty(self, GO.PCTOP, (0, 10)),
                    GUI.Text(self, GO.PCTOP, 'Game-specific commands', font=GO.FTITLE)
                ] + [
                    add_sett(f'"{i[0]}": {i[1]}') for i in gameself.cmds
                ])
                
                newG.sizeOfScreen = (self.size[0]/3, max(self.size[1]/2, sum([i.size[1] for i in newG.get()])))
                newG2.sizeOfScreen = (self.size[0]/3, max(self.size[1]/2, sum([i.size[1] for i in newG2.get()])))
        
        class items(Screen, RunInstantly):
            """
            /items ... : List all the entities and other things in the game and their ids and stuff!
            """
            def __init__(self, *args):
                super().__init__()
            
            def _LoadUI(self):
                self.layers[0].add('OverlayGUI')
                self['OverlayGUI'].append(GUI.Text(self, GO.PCTOP, """
Please note: If you used the internal icons it will appear blurry and without transparency. You're lucky I even provided you with THAT. PLEASE do not use them in your final game; the creator SPECIFICALLY said not to. I accept NO responsibility for you using this WHATSOEVER.
""", allowed_width=500))
                
                TOPLEFT = GO.PNEW((0, 0), (0, 1))
                self['OverlayGUI'].append(GUI.Text(self, TOPLEFT, 'All entities', font=GO.FTITLE))
                scr = GUI.ScrollableFrame(self, GO.PLCENTER, (self.size[0]/2-260, self.size[1]/3*2), (self.size[0]/2, 0))
                self['OverlayGUI'].append(scr)
                scr.layers[0].add('Alls')

                rainbow = GO.CRAINBOW()
                def func(e):
                    copy(e['uid'])
                    GUI.Toast(self, f'Copied "{e['uid']}" to clipboard!')
                for e in gameself.world.ldtk.defs['entities']:
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
                        UITile = pygame.transform.scale(gameself.world.ldtk.tilesets[e['tilesetId']].subsurface(
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
                
                scr.sizeOfScreen = (self.size[0]/2-260, max(self.size[1]/2, sum([i.size[1] for i in scr.get()])))
                
                TOPRIGHT = GO.PNEW((1, 0), (0, 1))
                self['OverlayGUI'].append(GUI.Text(self, TOPRIGHT, 'Entities in this level', font=GO.FTITLE))
                # TODO
        
        tb.addCmd('help', help)
        tb.addCmd('items', items)

        @tb.onWrong
        def onWrong(txt):
            alls = tb.popup.stacks.alls.keys()
            LTOP = [i for i in alls if i.weighting == (0, 0)][0]
            tb.popup['Main'].append(
                GUI.Text(tb.popup, LTOP, 'For help, use /help')
            )

    def __call__(self):
        """
        Play the game!
        """
        self.playing = True

        self.gameplayer = Player(self, self.world)
        if self.needCreateScene:
            self.needCreateScene = False
            self.curScene = self.curScene[0](self, **self.curScene[1])
        
        return super().__call__()
