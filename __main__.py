print('Loading modules...')
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Hide the annoying pygame thing
import pygame, os, json
from threading import Thread

from overlay import Overlay, tk
from graphics import Graphic
from graphics import graphics_options as GO
from utils import Player
from worldGen import World
from ldtk import LDtkAPP
from elementGen import NodeSelector, NodeEditor, modifyCats
G = Graphic()

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('AIHub')
    
    @G.CGraphic
    def world(self, event, world, element=None, aborted=False, newworld=False):
        """This plays a world.

        Args:
            world (World): The world.
        KWargs:
            newworld (bool, optional): Whether this is a new world or not. Defaults to False.
        """
        @G.Loading
        def load(self):
            self.player = Player(world, G.Loading, G.Abort)
        if event == GO.EFIRST:
            G.Container.lvl = 0
            success, cls = load()
            if not success: G.Abort()
            else:
                G.Container.Player = cls.player
                G.add_custom(cls.player)
    @G.CGraphic
    def world_edit(self, event, worldname, element=None, aborted=False):
        if event == GO.EFIRST:
            G.Container.current = 0
            @G.Loading
            def load(slf):
                slf.win = LDtkAPP()
                slf.win.open('data/worlds/%s/world.ldtk'%worldname)
                slf.win.wait_for_win()
                slf.overlay = Overlay((120, 50), (G.size[0]-20-110, 40), lambda: G.Abort()) # Covering nothing
                # We have to do it in the actual main thread
                def play(): G.Container.current = 1
                def addelm(): G.Container.current = 2
                tk.Button(slf.overlay(), text='Play!', command=play).pack() # TODO: replace with play button
                tk.Button(slf.overlay(), text='Add/edit elements!', command=addelm).pack()
            cont, res = load()
            if not cont: G.Abort()
            G.Container.win = res.win
            G.Container.over = res.overlay
        elif event == GO.EELEMENTCLICK:
            G.Container.win.kill()
            G.Abort()
        elif event == GO.ELOADUI:
            G.Clear()
            G.add_button('Exit', GO.CGREY, GO.PCCENTER)
        elif event == GO.ETICK:
            if G.Container.current != 0:
                def useMain(func):
                    def func2():
                        G.Container.over.hide()
                        G.BringToFront()
                        func()
                        t = Thread(target=G.Container.over.show, daemon=True) # For some reason showing it in the main thread causes problems
                        t.start()
                        G.Container.win.focusWIN()
                        G.Reload()
                    return func2
                if G.Container.current == 1:
                    @useMain
                    def play():
                        self.world(World(worldname))
                    play()
                elif G.Container.current == 2:
                    @useMain
                    @modifyCats
                    def addelm(categories):
                        r = True
                        categories.append(f'data/worlds/{worldname}/src/nodes')
                        while r:
                            r = False
                            ret = NodeSelector(G=G)
                            if ret is not None:
                                r = True
                                @G.Graphic
                                def options(event, element=None, aborted=False):
                                    if event == GO.ELOADUI:
                                        G.Clear()
                                        G.add_text(ret, GO.CBLACK, GO.PCTOP, GO.FTITLE)
                                        G.add_button('Back', GO.CGREY, GO.PCBOTTOM)
                                        G.add_button('Back to editor', GO.CNEW('orange'), GO.PCBOTTOM)
                                        G.add_button('Edit', GO.CGREEN, GO.PCCENTER)
                                        G.add_button('Apply', GO.CYELLOW, GO.PCCENTER)
                                    elif event == GO.EELEMENTCLICK:
                                        if element == 0:
                                            G.Abort()
                                        elif element == 1:
                                            return False
                                        elif element == 2:
                                            NodeEditor(ret, G)
                                            G.ab = False
                                        elif element == 3:
                                            pass
                                            # raise NotImplementedError('THIS IS STILL IN PROGRESS!')
                                if options() == False:
                                    r = False
                    addelm()
                G.Container.current = 0
                G.run = True
                G.ab = False
            if not G.Container.win.is_win_open():
                G.Abort()
                return False
            G.Container.win.make_full()
        elif event == GO.ELAST:
            G.Container.over.destroy()
            try:
                G.Container.win.kill()
            except: pass
    @G.CGraphic
    def world_select(self, event, element=None, aborted=False):
        if event == GO.EFIRST:
            @G.Loading
            def load(self):
                self.worlds = [i for i in os.scandir(os.path.join(os.getcwd(),'data/worlds')) if i.is_dir() and os.path.exists(os.path.join(os.getcwd(),'data/worlds/%s/dat.json'%i.name)) and os.path.exists(os.path.join(os.getcwd(),'data/worlds/%s/world.ldtk'%i.name))]
                self.worldinfo = [json.load(open('data/worlds/%s/dat.json'%i.name)) for i in self.worlds]
                self.subs = ['Go back to the previous page', 'Make a new world from scratch'] + [i['idea'] for i in self.worldinfo]
            cont, res = load()
            G.Container.res = res
            G.Container.txt = ''
            G.Container.Selection = None
            G.Container.prevpresses = []
            if not cont: G.Abort()
        elif event == GO.ELOADUI:
            G.Clear()
            G.add_text('World selection', GO.CBLACK, GO.PCTOP)
            G.add_text(G.Container.txt, GO.CBLUE, GO.PCTOP)
            G.add_button('Back', GO.CGREY, GO.PLTOP)
            G.add_button('New World', GO.CGREEN, GO.PLTOP)
            cols = GO.CRAINBOW()
            for i in G.Container.res.worldinfo:
                G.add_button(i['name'], next(cols), GO.PLCENTER)
            if G.Container.Selection is not None:
                uid, ng = G.add_Scrollable(GO.PCCENTER, (500, 700), (500, 700), bar=False)
                def close(_):
                    G.Container.Selection = None
                    G.Clear()
                    G.Reload()
                def play(_):
                    bef = G.Container.Selection
                    close(None)
                    self.world(World(bef))
                def edit(_):
                    bef = G.Container.Selection
                    close(None)
                    self.world_edit(bef)
                
                def still_in_progress(_):
                    raise NotImplementedError('THIS IS STILL IN PROGRESS!')

                LTOP = GO.PNEW([1, 1], GO.PSTACKS[GO.PLTOP][1])
                RBOT = GO.PNEW([-1, -1], GO.PSTACKS[GO.PRBOTTOM][1])
                ng.add_empty_space(LTOP, 20, 20)
                ng.add_button('Close', GO.CBLUE, LTOP, callback=close)
                ng.add_empty_space(GO.PLCENTER, 20, 0)
                ng.add_button('Play', GO.CGREEN, GO.PLCENTER, callback=play)
                ng.add_button('Edit', GO.CNEW('orange'), GO.PCCENTER, callback=edit)
                ng.add_empty_space(GO.PRCENTER, 20, 0)
                ng.add_button('Delete', GO.CRED, GO.PRCENTER, callback=still_in_progress)
                ng.add_empty_space(RBOT, 20, 20)
                ng.add_button('Options', GO.CGREY, RBOT, callback=still_in_progress)
        elif event == GO.ETICK:
            if G.touchingbtns != G.Container.prevpresses:
                G.Container.prevpresses = G.touchingbtns.copy()
                try: G.Container.txt = G.Container.res.subs[G.get_idx(G.touchingbtns[0])]
                except: G.Container.txt = ''
                G.Reload()
        elif event == GO.EELEMENTCLICK: # Passed 'element'
            if element == 0: # back
                return False
            elif element == 1: # make new world
                NumOTasks = 24 + 9 # 9 biome names
                dones = [False for _ in range(NumOTasks)]
                done = [False]
                async def wait(i):
                    while True:
                        if dones[i]: return True
                def NW(dones, done): # TODO: make a GUI screen to ask for title and description
                    def CB(txt):
                        G.Container.pbar.set_txt('{2}% ({0} / {1}): ' + txt.replace('...', '{3}'))
                        for i in range(len(dones)):
                            if dones[i] == False:
                                dones[i] = True
                                return
                    while G.Container.pbar == None:
                        pass
                    done[0] = World('newworld', 'New World', 'a new world', 16, 100, override=True, callback=CB)
                    for i in range(len(dones)): dones[i] = True
                t = Thread(target=NW, daemon=True, args=(dones, done))
                tasks = [wait(i) for i in range(NumOTasks)]
                G.Container.pbar = None
                t.start()
                G.PBLoading(tasks, 'Loading...')
                if done[0] is not False:
                    return self.world(done[0], newworld=True)
            else:
                G.Container.Selection = G.Container.res.worlds[element.uid-2].name
                G.Reload()
        elif event == GO.ELAST:
            pass
    @G.CGraphic
    def welcome(self, event, element=None, aborted=False):
        if event == GO.EFIRST:
            pass
        elif event == GO.ELOADUI:
            G.Clear()
            CBOT = GO.PNEW([1, 0], GO.PSTACKS[GO.PCBOTTOM][1])
            G.add_empty_space(CBOT, -50, 0)
            G.add_text('Welcome to Blaze Sudios! :)', GO.CBLUE, GO.PCCENTER, GO.FTITLE)
            G.add_button('Start', GO.CGREEN, CBOT)
            G.add_empty_space(CBOT, 20, 0)
            G.add_button('Tutorial', GO.CRED, CBOT)
        elif event == GO.EELEMENTCLICK:
            @G.Catch
            def start():
                if element == 0:
                    self.world_select()
                else:
                    raise NotImplementedError('THIS IS STILL IN PROGRESS!')
            start()
        elif event == GO.ELAST:
            pass

print('Finished loading modules! Launching app...')
if __name__ == '__main__':
    g = Game()
    G.BringToFront()
    g.welcome()

pygame.quit()
