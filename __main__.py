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
        if event == GO.TFIRST:
            G.Container.lvl = 0
            load()
        elif event == GO.TLOADUI:
            G.Clear()
            G.add_surface(G.Container.pg, GO.PFILL)
            G.add_text('World '+world.name+' level:%i'%G.Container.lvl, GO.CBLACK, GO.PCTOP, GO.FTITLE)
        elif event == GO.TTICK:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        G.Container.lvl -= 1
                        load()
                        G.Reload()
                    elif event.key == pygame.K_RIGHT:
                        G.Container.lvl += 1
                        load()
                        G.Reload()
            return True
        elif event == GO.TLAST:
            pass
    @G.CGraphic
    def world_select(self, event, element=None, aborted=False):
        if event == GO.TFIRST:
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
        elif event == GO.TLOADUI:
            G.Clear()
            G.add_text('World selection', GO.CBLACK, GO.PCTOP)
            G.add_text(G.Container.txt, GO.CBLUE, GO.PCTOP)
            G.add_button('Back', GO.CGREY, GO.PLTOP)
            G.add_button('New World', GO.CGREEN, GO.PLTOP)
            for i in G.Container.res['worldinfo']:
                G.add_button(i['name'], GO.CBLUE, GO.PLCENTER)
        elif event == GO.TTICK:
            if G.touchingbtns != G.Container.prevpresses:
                G.Container.prevpresses = G.touchingbtns.copy()
                try: G.Container.txt = G.Container.res['subs'][G.get_idx(G.touchingbtns[0])]
                except: G.Container.txt = ''
                G.Reload()
            return True
        elif event == GO.TELEMENTCLICK: # Passed 'element'
            idx = G.get_idx(element)
            if idx == 0: # back
                return None
            elif idx == 1: # make new world
                @G.Loading
                def NW(self): # TODO: make a GUI screen to ask fr title and description
                    self.world = World('newworld', 'New World', 'a new world', 25, quality=500)
                cont, res = NW()
                if cont:
                    self.world(res['world'], True)
            else:
                return self.world(World(G.Container.res['worlds'][idx-2].name))
        elif event == GO.TLAST:
            pass
    @G.CGraphic
    def welcome(self, event, element=None, aborted=False):
        if event == GO.TFIRST:
            pass
        elif event == GO.TLOADUI:
            G.Clear()
            CBOT = GO.PNEW([1, 0], GO.PSTACKS[GO.PCBOTTOM][1], 0)
            G.add_empty_space(CBOT, -50, 0)
            G.add_text('Welcome to AIHub! :)', GO.CBLUE, GO.PCCENTER, GO.FTITLE)
            G.add_button('Start', GO.CGREEN, CBOT)
            G.add_empty_space(CBOT, 20, 0)
            G.add_button('Tutorial', GO.CRED, CBOT)
        elif event == GO.TTICK:
            return True
        elif event == GO.TELEMENTCLICK: # Passed 'element'
            idx = G.get_idx(element)
            if idx == 0:
                self.world_select()
            else: print('Tutorial coming soon :)')
        elif event == GO.TLAST:
            pass

if __name__ == '__main__':
    g = Game()
    g.welcome()

pygame.quit()
