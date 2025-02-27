if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    from title import TitleScreen
    l = TitleScreen(600, 50, 19) # 17
    l(5, 'Loading{3}')
    def nxt(name):
        l.update()
        if 'Loading' in name:
            l.set_txt(name.replace('...', '{3}')+' ({2}%)')
        else:
            l.set_txt('Loading '+name+'{3} ({2}%)')

    nxt('Logging')
    import logging
    from title import CustomHandler
    logger = logging.getLogger()
    handle = CustomHandler(lambda msg: None if 'Loading' not in msg and '...' not in msg else nxt(msg))
    handle.setLevel(logging.INFO)
    logger.addHandler(handle)
    logger.setLevel(logging.INFO)
    nxt('Core modules')
    import os, json
    import multiprocessing as MP
    nxt('Pygame')
    import pygame
    nxt('Graphics')
    from BlazeSudio.graphics import Graphic, thread_with_exception
    import BlazeSudio.graphics.options as GO
    nxt('Overlay')
    from BlazeSudio.overlay import Overlay, tk
    nxt('Player')
    from BlazeSudio.utils import Player
    nxt('World generator')
    from BlazeSudio.worldGen import World
    nxt('LDtk app')
    from BlazeSudio.ldtk import LDtkAPP
    nxt('Demos')
    import demos
    from title import wrapdemo
    nxt('Threads')
    from threading import Thread
    nxt('ElementGen')
    from BlazeSudio.elementGen import NodeSelector, NodeEditor, modifyCats
    nxt('Cleaning up and starting...')
    logger.handlers.clear()
    logger.setLevel(logging.WARNING)
    l.join()
    G = Graphic()
    G.set_caption('Blaze Sudios!', pygame.image.load('images/FoxIconSmall.png'))

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
                    slf.overlay = Overlay((120, 50), (G.size[0]-20-110, 40), lambda: G.Abort()) # Covering nothing
                    # We have to do it in the actual main thread
                    def play(): G.Container.current = 1
                    def qact(): G.Container.current = 2
                    def editgfs(): G.Container.current = 3
                    tk.Button(slf.overlay(), text='Play!', command=play).pack() # TODO: replace with play button
                    tk.Button(slf.overlay(), text='Quick action!', command=qact).pack()
                    tk.Button(slf.overlay(), text='Edit game funcs!', command=editgfs).pack()
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
                            func()
                            t = Thread(target=G.Container.over.show, daemon=True) # For some reason showing it in the main thread causes problems
                            t.start()
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
                        def quickacts(categories):
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
                                            G.add_button('Back to editor', GO.CORANGE, GO.PCBOTTOM)
                                            # TODO: copy/move to/from world-specific nodes
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
                                                G.Toast('THIS IS STILL IN PROGRESS!')
                                    if options() == False:
                                        r = False
                        quickacts()
                    elif G.Container.current == 3:
                        @useMain
                        @G.Graphic
                        def editgfs(event, element=None, aborted=False):
                            pass
                    G.Container.current = 0
                    G.run = True
                    G.ab = False
            elif event == GO.ELAST:
                G.Container.over.destroy()
                try:
                    G.Container.win.kill()
                except: pass
        @G.Catch
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
                        G.Toast('THIS IS STILL IN PROGRESS!')

                    LTOP = GO.PNEW((1, 1), GO.PLTOP.func)
                    RBOT = GO.PNEW((-1, -1), GO.PRBOTTOM.func)
                    ng.add_empty_space(LTOP, 20, 20)
                    ng.add_button('Close', GO.CBLUE, LTOP, callback=close)
                    ng.add_empty_space(GO.PLCENTER, 20, 0)
                    ng.add_button('Play', GO.CGREEN, GO.PLCENTER, callback=play)
                    ng.add_button('Edit', GO.CORANGE, GO.PCCENTER, callback=edit)
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
                    tasks = [wait(i) for i in range(NumOTasks)]
                    pbar, func = G.PBLoading(tasks, 'Loading...')
                    def NW(dones, done): # TODO: make a GUI screen to ask for title and description
                        def CB(txt):
                            pbar.set_txt('{2}% ({0} / {1}): ' + txt.replace('...', '{3}'))
                            for i in range(len(dones)):
                                if dones[i] == False:
                                    dones[i] = True
                                    return
                        done[0] = World('newworld', 'New World', 'a new world', 16, 100, override=True, callback=CB)
                        for i in range(len(dones)): dones[i] = True
                    t = thread_with_exception(target=NW, daemon=True, args=(dones, done))
                    t.start()
                    func()
                    t.raise_exception()
                    if done[0] is not False:
                        return self.world(done[0], newworld=True)
                else:
                    G.Container.Selection = G.Container.res.worlds[element.uid-2].name
                    G.Reload()
        
        @G.CGraphic
        def run_demo(self, event, demoname, element=None, **__):
            if event == GO.EFIRST:
                G.Container.msgs = []
                ev = MP.Event()
                G.Container.has_started = MP.Event()
                G.Container.inputting = [False, ev, None]
                G.Container.Q = MP.Queue()
                G.Container.p = MP.Process(target=wrapdemo, args=(G.Container.Q, ev, G.Container.has_started, demoname), daemon=True)
                G.Container.p.start()
            elif event == GO.ELOADUI:
                G.Clear()
                G.add_text(demoname, GO.CBLACK, GO.PCTOP, GO.FTITLE)
                if not G.Container.has_started.is_set():
                    G.add_text('Loading...', GO.CBLACK, GO.PCCENTER, allowed_width=900)
                else: 
                    G.add_text(''.join(G.Container.msgs), GO.CBLACK, GO.PCCENTER, allowed_width=900)
                    if G.Container.inputting[0]:
                        BOT = GO.PNEW((1, 0), GO.PCBOTTOM.func)
                        G.add_text(G.Container.inputting[2], GO.CBLACK, BOT)
                        G.add_input(BOT, resize=GO.RWIDTH)
            elif event == GO.ETICK:
                if not G.Container.p.is_alive():
                    G.Abort()
                    return
                try:
                    resp = G.Container.Q.get_nowait()
                    if resp[0] == 0:
                        G.Container.msgs.append(resp[1]) # printed
                    elif resp[0] == 1:
                        G.Container.inputting[0] = True
                        G.Container.inputting[2] = resp[1]
                    elif resp[0] == 2:
                        @G.Catch
                        def raiseError():
                            raise resp[1]
                        raiseError()
                    G.Reload()
                except:
                    pass
            elif event == GO.EELEMENTCLICK: # This will be the inputbox
                G.Container.Q.put(element.txt.strip())
                G.Container.inputting[1].set()
                G.Container.inputting[0] = False
            elif event == GO.ELAST:
                if G.Container.p.is_alive():
                    G.Container.p.kill()
                    G.Container.p.join()
        
        @G.CGraphic
        def demoScreen(self, event, *_, **__):
            if event == GO.ELOADUI:
                G.Clear()
                ds = [i for i in dir(demos) if not i.startswith('__') and i not in [
                    'Thread', 'environ', 'CATEGORYNAMES'
                ]]
                dems = {}
                demcats = {}
                for i in ds:
                    cat = demos.CATEGORYNAMES[i[0]]
                    demcats[i[1:]] = i
                    if cat in dems:
                        dems[cat].append(i[1:])
                    else:
                        dems[cat] = [i[1:]]
                
                font = GO.FREGULAR
                aw = G.size[0]-50
                
                size = (G.size[0], max(
                    sum([
                        font.render(i, GO.CBLACK, allowed_width=aw).get_size()[1]+20 for i in ds
                    ])+sum([
                        font.render(i, GO.CBLACK, allowed_width=aw).get_size()[1]  for i in dems
                    ]),
                G.size[1])+40)
                LTOP = GO.PNEW((1, 1), GO.PLTOP.func)
                _, newG = G.add_Scrollable(GO.PLTOP, G.size, size)
                newG.add_empty_space(LTOP, 20, 20)
                newG.add_button('Back', GO.CGREY, LTOP, font=font, callback=G.Abort)
                newG.add_empty_space(GO.PCTOP, 0, 20)
                col = GO.CRAINBOW()
                for i in dems:
                    newG.add_text(i, GO.CBLACK, GO.PCTOP, font, aw)
                    for j in dems[i]:
                        real = demcats[j]
                        newG.add_button(j, next(col), GO.PCTOP, font=font, allowed_width=aw, callback=lambda _, n=real: self.run_demo(n))
        
        @G.CGraphic
        def welcome(self, event, element=None, aborted=False):
            if event == GO.ELOADUI:
                G.Clear()
                CBOT = GO.PNEW((1, 0), GO.PCBOTTOM.func)
                G.add_empty_space(CBOT, -100, 0)
                G.add_text('Welcome to...\nBlaze Sudios! 🦊', GO.CBLUE, GO.PCCENTER, GO.FTITLE)
                G.add_button('Start', GO.CGREEN, CBOT)
                G.add_empty_space(CBOT, 20, 0)
                G.add_button('Demos', GO.CBLUE, CBOT)
                G.add_empty_space(CBOT, 20, 0)
                G.add_button('Tutorial', GO.CRED, CBOT)
            elif event == GO.EELEMENTCLICK:
                if element == 0:
                    self.world_select()
                elif element == 1:
                    self.demoScreen()
                else:
                    G.Toast('THIS IS STILL IN PROGRESS!')

    g = Game()
    g.welcome()
    pygame.quit()
