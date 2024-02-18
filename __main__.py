print('Loading modules... (may take a while)')
import pygame, os, json
from graphics import Graphic
from graphics import graphics_options as GO
from utils import World
from ldtk import LDtkAPP
from threading import Thread
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
        def load():
            @G.Loading
            def lo(self):
                self.ret = False
                self.ret = world.get_pygame(G.Container.lvl)
            out = lo()
            if not out[0]: G.Abort()
            G.Container.pg = out[1]['ret']
            if not G.Container.pg: G.Abort()
        if event == GO.EFIRST:
            G.Container.lvl = 0
            load()
        elif event == GO.ELOADUI:
            G.Clear()
            G.add_surface(G.Container.pg, GO.PFILL)
            G.add_text('World '+world.name+' level:%i'%G.Container.lvl, GO.CBLACK, GO.PCTOP, GO.FTITLE)
        elif event == GO.ETICK:
            return True
        elif event == GO.EEVENT: # Passed 'element' (but is event)
            if element.type == pygame.KEYDOWN:
                if element.key == pygame.K_LEFT:
                    G.Container.lvl -= 1
                    load()
                    G.Reload()
                elif element.key == pygame.K_RIGHT:
                    G.Container.lvl += 1
                    load()
                    G.Reload()
        elif event == GO.ELAST:
            pass
    @G.CGraphic
    def world_edit(self, event, worldname, element=None, aborted=False):
        if event == GO.EFIRST:
            @G.Loading
            def load(self):
                self.win = LDtkAPP()
                self.win.open('data/worlds/%s/world.ldtk'%worldname)
                self.win.wait_for_win()
            cont, res = load()
            if not cont: G.Abort()
            G.Container.win = res['win']
        elif event == GO.EELEMENTCLICK:
            G.Container.win.kill()
            G.Abort()
        elif event == GO.ELOADUI:
            G.Clear()
            G.add_button('Exit', GO.CGREY, GO.PCCENTER)
        elif event == GO.ETICK:
            if not G.Container.win.is_win_open():
                G.Abort()
                return
            G.Container.win.make_full()
            return True
        elif event == GO.ELAST:
            pass # TODO: stop the thread from running to close the program
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
            for i in G.Container.res['worldinfo']:
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
                ng.add_button('Close', GO.CBLUE, GO.PLTOP, callback=close)
                ng.add_button('Play', GO.CGREEN, GO.PLCENTER, callback=play)
                ng.add_button('Edit', GO.CNEW('orange'), GO.PCCENTER, callback=edit)
                ng.add_button('Delete', GO.CRED, GO.PRCENTER, callback=lambda _: print('STILL IN PROGRESS!'))
                ng.add_button('Options', GO.CGREY, GO.PRBOTTOM, callback=lambda _: print('STILL IN PROGRESS!'))
        elif event == GO.ETICK:
            if G.touchingbtns != G.Container.prevpresses:
                G.Container.prevpresses = G.touchingbtns.copy()
                try: G.Container.txt = G.Container.res['subs'][G.get_idx(G.touchingbtns[0])]
                except: G.Container.txt = ''
                G.Reload()
            return True
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
                G.Container.Selection = G.Container.res['worlds'][element.uid-2].name
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
        elif event == GO.ETICK:
            return True
        elif event == GO.EELEMENTCLICK:
            if element == 0:
                self.world_select()
            else: print('Tutorial coming soon :)')
        elif event == GO.ELAST:
            pass

print('Finished loading modules! Launching app...')
if __name__ == '__main__':
    g = Game()
    g.welcome()

pygame.quit()
