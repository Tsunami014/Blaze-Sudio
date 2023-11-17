# TODO: make each file not need to be dependant on python files from above folders
import pygame, os, json
from graphics import Graphic
from graphics import graphics_options as GO
from utils import World
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
            def l(self):
                self.ret = False
                self.ret = world.get_pygame(G.Container.lvl)
            out = l()
            if not out[0]: G.Abort()
            G.Container.pg = out[1]['ret']
            if G.Container.pg == False: G.Abort()
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
    def world_select(self, event, element=None, aborted=False):
        if event == GO.EFIRST:
            @G.Loading
            def load(self):
                self.worlds = [i for i in os.scandir('data/worlds') if i.is_dir() and os.path.exists('data/worlds/%s/dat.json'%i.name) and os.path.exists('data/worlds/%s/world.ldtk'%i.name)]
                self.worldinfo = [json.load(open('data/worlds/%s/dat.json'%i.name)) for i in self.worlds]
                self.subs = ['Go back to the previous page', 'Make a new world from scratch'] + [i['idea'] for i in self.worldinfo]
            cont, res = load()
            G.Container.res = res
            G.Container.txt = ''
            G.Container.prevpresses = []
            if not cont: G.Abort()
        elif event == GO.ELOADUI:
            G.Clear()
            G.add_text('World selection', GO.CBLACK, GO.PCTOP)
            G.add_text(G.Container.txt, GO.CBLUE, GO.PCTOP)
            G.add_button('Back', GO.CGREY, GO.PLTOP)
            G.add_button('New World', GO.CGREEN, GO.PLTOP)
            for i in G.Container.res['worldinfo']:
                G.add_button(i['name'], GO.CBLUE, GO.PLCENTER)
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
                @G.Loading
                def NW(self): # TODO: make a GUI screen to ask fr title and description
                    self.world = World('newworld', 'New World', 'a new world', 25, quality=500)
                cont, res = NW()
                if cont:
                    return self.world(res['world'], True)
            else:
                return self.world(World(G.Container.res['worlds'][element.uid-2].name))
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
            G.add_text('Welcome to AIHub! :)', GO.CBLUE, GO.PCCENTER, GO.FTITLE)
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

if __name__ == '__main__':
    g = Game()
    g.welcome()

pygame.quit()
