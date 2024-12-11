# Main STUFF
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def NodeEditorDemo():
    try:
        print('Press cancel to run the demo without saving to any file.\n\
If you specify an existing file and it asks you are you sure you want to overwrite it, do not fret. \
It will first read the file, then overwrite it when you save.')
        from tkinter.filedialog import asksaveasfilename
        f = asksaveasfilename(filetypes=[('Element file', '*.elm')], defaultextension='.elm')
        if not f:
            f = None
    except ImportError:
        f = None
    from BlazeSudio.elementGen import NodeEditor
    NodeEditor(f)

def GraphicsDemo():
    import BlazeSudio.graphics.options as GO
    from BlazeSudio.graphics import Screen, Loading, GUI
    from BlazeSudio.graphics.GUI.base import HiddenStatus
    from BlazeSudio.graphics.GUI.base import ReturnState
    import pygame
    from time import sleep
    @Loading
    def test_loading(slf):
        for slf.i in range(10):
            sleep(1)
    
    class Test(Screen):
        def __init__(self, txt):
            super().__init__(GO.CWHITE)
            self.txt = txt
        
        def _LoadUI(self): # Load the graphics in!
            CTOP = GO.PNEW((0.5, 0), (1, 0), (True, False)) # Bcos usually the Center Top makes the elements stack down, so I make a new thing that stacks sideways
            LBOT = GO.PNEW((0, 1), (0, -1))
            self.layers[0].add_many([
                # You can name these whatever you want, but I like to keep them the same as the type.
                'TB',
                'texts',
                'space',
                'buttons',
                'events',
                'speshs',
                'endElms', # These will be the ones I find in the GO.ELAST event
            ])
            # I chose this because you can see the different sections of the screen, but you can do what you want; as long as they end up on the list it's ok.
            self['TB'].append(GUI.TerminalBar(self))

            f = GUI.ScaledByFrame(self, GO.PRBOTTOM, (500, 400))
            self['speshs'].append(f)
            f.layers[0].add('Alls')
            LTOP = GO.PNEW((0, 0), (0, 1))
            f['Alls'].extend([
                GUI.Text(f, LTOP, 'Scaled Frame', GO.CBLUE),
                GUI.Empty(f, LTOP, (0, 15)),
                GUI.Text(f, LTOP, 'Change scale:', GO.CGREEN),
            ])
            self.changeScale = GUI.NumInputBox(f, LTOP, 100, GO.RHEIGHT, start=2, min=1, placeholdOnNum=None)
            f['Alls'].append(self.changeScale)

            self['texts'].append(GUI.Text(self, GO.PCCENTER, 'This is a cool thing', GO.CBLUE))
            self.Invisi_T = GUI.Text(self, GO.PCCENTER, 'Sorry, I meant a cool TEST', GO.CRED)
            self['texts'].append(self.Invisi_T)
            self.txt = GUI.Text(self, GO.PCCENTER, self.txt, GO.CGREEN)
            self['texts'].append(self.txt)
            self.inp = GUI.InputBox(self, GO.PCCENTER, 500, GO.RHEIGHT, font=GO.FFONT)
            self['endElms'].append(self.inp)
            self['space'].append(GUI.Empty(self, GO.PCCENTER, (0, 50)))
            self['endElms'].append(GUI.NumInputBox(self, GO.PCCENTER, 100, font=GO.FFONT, min=-255, max=255))
            self['space'].append(GUI.Empty(self, GO.PCCENTER, (0, 50)))
            self['endElms'].append(GUI.DropdownButton(self, GO.PCCENTER, ['HI', 'BYE']))

            self['space'].append(GUI.Empty(self, LBOT, (0, 20)))
            self['buttons'].append(GUI.Button(self, LBOT, GO.CYELLOW, 'Button 1 :D'))
            self['texts'].append(GUI.Text(self, LBOT, 'Buttons above [^] and below [v]', GO.CBLUE))
            self.PopupBtn = GUI.Button(self, LBOT, GO.CMAUVE, 'Popup test')
            self['buttons'].append(self.PopupBtn)
            self.TextboxBtn = GUI.Button(self, LBOT, GO.CBLUE, 'Textbox test')
            self['buttons'].append(self.TextboxBtn)
            self.LoadingBtn = GUI.Button(self, LBOT, GO.CGREEN, 'Loading test')
            self['buttons'].append(self.LoadingBtn)
            self.exitbtn = GUI.Button(self, GO.PLCENTER, GO.CRED, 'EXIT', GO.CWHITE, func=lambda: self.Abort())
            self['buttons'].append(self.exitbtn)

            self['texts'].extend([
                GUI.Text(self, CTOP, 'Are you '),
                GUI.Text(self, CTOP, 'happy? ', GO.CGREEN),
                GUI.Text(self, CTOP, 'Or sad?', GO.CRED)
            ])

            self.switches = [
                GUI.Switch(self, GO.PRTOP, 40, 2),
                GUI.Switch(self, GO.PRTOP, default=True),
            ]
            self['endElms'].extend(self.switches)
            self.colour = GUI.ColourPickerBTN(self, GO.PRTOP)
            self['endElms'].append(self.colour)

            L = GUI.GridLayout(self, GO.PCBOTTOM, outline=5)
            self['speshs'].append(L)
            self.sw = GUI.Switch(L, L.LP)
            L.grid = [
                [GUI.Text(L, L.LP, 'HI'), GUI.Text(L, L.LP, 'HELLO'), GUI.Text(L, L.LP, 'BYE')],
                [GUI.Text(L, L.LP, 'HEHE'), GUI.Text(L, L.LP, 'YES'), GUI.Text(L, L.LP, 'NO')],
                [GUI.Text(L, L.LP, 'HAVE'), GUI.Text(L, L.LP, 'A'), GUI.Text(L, L.LP, 'NICEDAY')],
                [GUI.Button(L, L.LP, GO.CORANGE, 'Hello!'), None, self.sw]
            ]

            TOPLEFT = GO.PSTATIC(10, 10) # Set a custom coordinate that never changes
            S = GUI.ScrollableFrame(self, TOPLEFT, (250, 200), (400, 450))
            self['speshs'].append(S)
            # This is another way of setting out your Stuff; having everything under one name.
            S.layers[0].add('Alls')
            S['Alls'].extend([
                GUI.Empty(S, GO.PCTOP, (0, 10)),
                GUI.Text(S, GO.PCTOP, 'Scroll me!', GO.CBLUE),
                GUI.Empty(S, GO.PCTOP, (0, 50)),
                GUI.InputBox(S, GO.PCTOP, 200, GO.RHEIGHT, weight=GO.SWLEFT),
                GUI.Empty(S, GO.PCTOP, (0, 50)),
                GUI.Button(S, GO.PCTOP, GO.CGREEN, 'Press me!', func=lambda: self.txt.set('You pressed the button in the Scrollable :)')),
                GUI.Empty(S, GO.PCTOP, (0, 50)),
                GUI.Text(S, GO.PCTOP, 'Auto adjust scrollable height', GO.CORANGE, allowed_width=200),
                GUI.Switch(S, GO.PCTOP, speed=0.5)
            ])
        def _Tick(self): # This runs every 1/60 secs (each tick)
            # Return False if you want to quit the screen. This is not needed if you never want to do this.
            self['speshs'][0].scale = self.changeScale.get()
            S = self['speshs'][2]
            e = S['Alls'][-1]
            if e.get():
                S.sizeOfScreen = (S.sizeOfScreen[0], e.stackP()[1]+e.size[1]+30)
            else:
                S.sizeOfScreen = (S.sizeOfScreen[0], 450)
        def _ElementClick(self, obj): # Some UI element got clicked!
            if obj.type == GO.TBUTTON:
                # This gets passed 'obj': the element that got clicked.
                if obj == self.LoadingBtn:
                    succeeded, ret = test_loading()
                    self.txt.set('Ran for %i seconds%s' % (ret.i+1, (' Successfully! :)' if succeeded else ' And failed :(')))
                elif obj == self.TextboxBtn:
                    bot = GO.PNEW((0.5, 1), (0, 0), (True, False))
                    dialog_box = GUI.TextBoxAdv(self, bot, text='HALOOO!!')
                    dialog_box.set_indicator()
                    dialog_box.set_portrait()
                    self['events'].append(dialog_box)
                    self.idx = 0
                elif obj == self.PopupBtn:
                    pop = GUI.PopupFrame(self, GO.PCCENTER, (350, 300))
                    pop.layers[0].add('Alls')
                    def rmpop(pop):
                        pop.remove()
                        return ReturnState.DONTCALL
                    pop['Alls'].extend([
                        GUI.Empty(pop, GO.PCTOP, (0, 10)),
                        GUI.Text(pop, GO.PCTOP, 'Popup', font=GO.FTITLE),
                        GUI.Text(pop, GO.PCCENTER, 'This is an example of a popup!', allowed_width=250),
                        GUI.Button(pop, GO.PRTOP, GO.CYELLOW, '❌', func=lambda p=pop: rmpop(p)),
                        GUI.Empty(pop, GO.PCBOTTOM, (0, 10)),
                        GUI.InputBox(pop, GO.PCBOTTOM, 250, GO.RNONE, 'Example textbox', maxim=16),
                    ])
                    self['events'].append(pop) # I know it's not an event, but o well.
                else:
                    self.txt.set(obj.txt) # put name of button in middle
            elif obj.type == GO.TTEXTBOX:
                if self.idx == 0:
                    obj.set("Happy coding!")
                    self.idx = 1
                else: 
                    obj.remove()
            elif obj.type == GO.TINPUTBOX:
                self.txt.set(obj.get().strip())
            elif obj.type == GO.TSWITCH:
                if obj == self.sw:
                    if obj.get():
                        self.Invisi_T.hiddenStatus = HiddenStatus.GONE
                    else:
                        self.Invisi_T.hiddenStatus = HiddenStatus.SHOWING
        def _Event(self, event): # When something like a mouse or keyboard button is pressed. Is passed 'element' too, but this time it is an event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:
                    self['events'].append(GUI.Toast(self, 'Saved! (Don\'t worry - this does nothing)', GO.CGREEN))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
                opts = ['HI', 'BYE', 'HI AGAIN']
                def dropdownSelect(resp):
                    if isinstance(resp, int):
                        self.txt.set(opts[resp])
                self['events'].append(GUI.Dropdown(self, pygame.mouse.get_pos(), opts, func=dropdownSelect))
        def _Last(self, aborted):
            # This also gets passed 'aborted': Whether you aborted or exited the screen
            S = self['speshs'][2]
            return { # Whatever you return here will be returned by the function
                'Aborted?': aborted, 
                'endElms': self['endElms']+[
                    # These are the input and the switch
                    S['Alls'][3],
                    S['Alls'][-1],
                ]}
    
    print(Test('Right click or press anything or press ctrl+s!')())
    pygame.quit() # this here for very fast quitting

def LoremGraphicsDemo():
    from BlazeSudio.graphics import Graphic, options as GO, GUI
    G = Graphic()
    G.layers[0].add('speshs')
    @G.Screen
    def test(event, element=None, aborted=False):
        if event == GO.ELOADUI:
            @G.Loading
            def load(slf):
                S2 = GUI.ScrollableFrame(G, GO.PCCENTER, (900, 700), (2000, 11000))
                S2.layers[0].add('alls')
                with open('demoFiles/lorem.txt') as f:
                    lorem = f.read()
                S2['alls'].append(GUI.Text(S2, GO.PCTOP, lorem, allowed_width=1900))
                G['speshs'].append(S2)
            load()

    test()

def ThemePgDemo():
    import demoFiles.themePlayground as themePlayground  # noqa: F401

def CollisionsDemo(debug=False):
    if debug:
        from BlazeSudio.debug import collisions  # noqa: F401
    from demoFiles import collisionsDemo  # noqa: F401

def WrapBasicDemo():
    from BlazeSudio.collisions import Point
    from BlazeSudio.utils.wrap import makeShape
    import pygame
    import sys
    pygame.init()

    win = pygame.display.set_mode()
    pygame.display.toggle_fullscreen()

    main = makeShape.MakeShape(100)

    conns = {
        '|': 0,
        '-': 90,
        '/': -45,
        '\\': 45,
    }

    run = True
    heldSegment = None
    selectedSegment = None
    movingMode = False
    while run:
        newMM = pygame.key.get_mods() & pygame.KMOD_ALT
        if newMM and not movingMode:
            try:
                main.makeShape()
            except Exception as e:
                print(f'There was an error generating your shape: {type(e)} - {e}', file=sys.stderr)
        movingMode = newMM

        selectedJoint = (None, None)
        if not movingMode:
            mp = pygame.mouse.get_pos()
            for idx in range(len(main.joints)):
                i = main.joints[idx]
                if (i[0]-mp[0])**2+(i[1]-mp[1])**2 <= 5**2:
                    selectedJoint = (idx, i)
                    break
        
        boxes = len(conns)
        gap = 10
        boxSze = 30
        
        if selectedSegment is not None:
            h = boxSze+gap*2
            w = (boxSze+gap)*boxes+gap
            x, y = (selectedSegment[0][0][0]+selectedSegment[0][1][0]-w)/2, min(selectedSegment[0][0][1], selectedSegment[0][1][1])-h-gap*3

            SelectedR = pygame.Rect(x, y, w, h)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_SPACE:
                    if (not movingMode) and (selectedJoint[0] is None):
                        main.insert_straight(pygame.mouse.get_pos()[0])
                elif event.key == pygame.K_r:
                    main = makeShape.MakeShape(100)
                    heldSegment = None
                    selectedJoint = (None, None)
                    selectedSegment = None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if not movingMode:
                    heldSegment = selectedJoint[0]

                    if selectedSegment is None or not SelectedR.collidepoint(event.pos):
                        selectedSegment = None
                        mp = Point(*event.pos)
                        idx = 0
                        for seg in main.collSegments:
                            p = seg.closestPointTo(mp)
                            if (p[0]-event.pos[0])**2+(p[1]-event.pos[1])**2 <= 5**2:
                                selectedSegment = (seg, idx)
                                break
                            idx += 1
                    else:
                        for i in range(boxes):
                            r = pygame.Rect(x+(boxSze+gap)*i+gap, y+gap, boxSze, boxSze)
                            if r.collidepoint(event.pos):
                                val = list(conns.values())[i]
                                main.setAngs[selectedSegment[1]] = val
                                break
        
        if pygame.key.get_pressed()[pygame.K_s]:
            if (not movingMode) and (selectedJoint[0] is None):
                main.insert_straight(pygame.mouse.get_pos()[0])
        
        if heldSegment is not None and (not pygame.mouse.get_pressed()[0]):
            heldSegment = None
        
        win.fill((10, 10, 10))

        y = win.get_height()/2
        x = (win.get_width()+main.width)/2
        
        if movingMode:
            selectedSegment = None
            heldSegment = None
            if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                main.recentre(*pygame.mouse.get_pos())
        else:
            if heldSegment is not None:
                selectedSegment = None
                newx = pygame.mouse.get_pos()[0]
                if heldSegment > 0:
                    newx = min(newx, main.joints[heldSegment-1][0])
                if heldSegment < len(main.joints)-1:
                    newx = max(newx, main.joints[heldSegment+1][0])
                if [round(j[0],6) for j in main.joints].count(round(newx,6)) > 1:
                    main.delete(heldSegment)
                    heldSegment = None
                else:
                    main.joints[heldSegment] = (newx, main.joints[heldSegment][1])
                main.recalculate_dists()
            else:
                main.joints[0] = (x, y)
                main.straighten()

        if selectedSegment is not None:
            pygame.draw.line(win, (255, 165, 10), selectedSegment[0][0], selectedSegment[0][1], 15)

        segs = main.segments
        for i in range(len(segs)):
            if main.setAngs[i] is not None:
                col = (10, 50, 255)
            else:
                col = (255, 255, 255)
            pygame.draw.line(win, col, segs[i][0], segs[i][1], 10)
        idx = 0
        for j in main.joints:
            if j == selectedJoint[1]:
                pygame.draw.circle(win, (255, 100, 100), j, 5)
            elif idx in (0, len(main.joints)-1):
                pygame.draw.circle(win, (200, 50, 200), j, 5)
            else:
                pygame.draw.circle(win, (100, 100, 255), j, 5)
            idx += 1
        
        if selectedSegment is not None:
            h = boxSze+gap*2
            w = (boxSze+gap)*boxes+gap
            x, y = (selectedSegment[0][0][0]+selectedSegment[0][1][0]-w)/2, min(selectedSegment[0][0][1], selectedSegment[0][1][1])-h-gap*3
            pygame.draw.rect(win, (125, 125, 125), (x, y, w, h), border_radius=4)
            vals = list(conns.values())
            f = pygame.font.Font(None, boxSze)
            for i in range(boxes):
                r = pygame.Rect(x+(boxSze+gap)*i+gap, y+gap, boxSze, boxSze)
                if vals[i] == main.setAngs[selectedSegment[1]]:
                    if r.collidepoint(pygame.mouse.get_pos()):
                        col = (255, 50, 255)
                    else:
                        col = (10, 50, 255)
                else:
                    if r.collidepoint(pygame.mouse.get_pos()):
                        col = (255, 255, 10)
                    else:
                        col = (255, 255, 255)
                pygame.draw.rect(win, col, r, border_radius=4)
                txt = f.render(list(conns.keys())[i], 1, (0, 0, 0))
                win.blit(txt, (r.x+(r.w-txt.get_width())/2, r.y+(r.h-txt.get_height())/2))
        
        if movingMode:
            polys = main.generateBounds(100)

            # Outer Polygon
            ps = list(polys[0])
            for p in ps:
                pygame.draw.circle(win, (125, 125, 125), p, 3)
            for i in range(len(ps)-1):
                pygame.draw.line(win, (125, 125, 125), ps[i], ps[i+1], 3)
            
            # Inner Shapes[Line]
            for i in polys[2]:
                pygame.draw.line(win, (125, 125, 125), i[0], i[1], 3)

        pygame.display.update()

def WrapDemo():
    from BlazeSudio.graphics import Graphic, GO, GUI
    from BlazeSudio.utils.wrap import wrapSurface, Segment
    import pygame
    G = Graphic(GO.CGREY)
    G.layers[0].add('Main')
    G.insert_layer().add('Top')

    def makeSur():
        topF = G.Container.topF
        news = pygame.Surface((1, 2))
        news.set_at((0, 0), topF['Main'][1].get())
        news.set_at((0, 1), topF['Main'][3].get())
        news2 = pygame.transform.smoothscale(news, (topF['Main'][5].get(), topF['Main'][7].get()))
        G.Container.inputSur = news2
        topF['Main'][-1].set(news2)
        G.Container.segs = []
        G.Container.cursegidx = None
    
    @G.Screen
    def screen(event, element=None, aborted=False):
        if event == GO.ELOADUI:
            G.Clear()
            G.Container.segs = []
            G.Container.cursegidx = None
            topF = GUI.BaseFrame(G, GO.PCTOP, (G.size[0], G.size[1]//2), 2)
            topF.layers[0].add('Main')
            G.Container.topF = topF
            botF = GUI.BaseFrame(G, GO.PCTOP, (G.size[0], G.size[1]//2), 2)
            botF.layers[0].add('Main')
            G.Container.botF = botF

            G['Main'].extend([topF, botF])

            G.Container.GObtn = GUI.Button(G, GO.PCCENTER, GO.CORANGE, 'Wrap!')
            G['Top'].append(G.Container.GObtn)

            LTOP = GO.PNEW((0, 0), (0, 1))
            topF['Main'].extend([
                GUI.Text(topF, LTOP, 'Colour 1'),
                GUI.ColourPickerBTN(topF, LTOP),
                GUI.Text(topF, LTOP, 'Colour 2'),
                GUI.ColourPickerBTN(topF, LTOP, default=(10,255,50)),
                GUI.Text(topF, LTOP, 'Width'),
                GUI.NumInputBox(topF, LTOP, 100, GO.RHEIGHT, start=500, min=1, max=1500, placeholdOnNum=None),
                GUI.Text(topF, LTOP, 'Height'),
                GUI.NumInputBox(topF, LTOP, 100, GO.RHEIGHT, start=100, min=1, max=500, placeholdOnNum=None),
            ])

            RTOP = GO.PNEW((1, 0), (0, 1))
            G.Container.offset = len(topF['Main'])
            topF['Main'].extend([
                GUI.Text(topF, RTOP, 'Ri'),
                GUI.NumInputBox(topF, RTOP, 100, GO.RHEIGHT, start=0, min=0, max=500, placeholdOnNum=None),
            ])

            topF['Main'].append(GUI.Text(topF, GO.PCTOP, 'INPUT IMAGE', font=GO.FTITLE))

            def customImg(img):
                topF['Main'][-1].set(pygame.image.load(img))
                G.Container.segs = []
                G.Container.cursegidx = None

            rainbow = GO.CRAINBOW()
            topF['Main'].extend([
                GUI.Button(topF, GO.PLBOTTOM, next(rainbow), 'Iris',   func=lambda: customImg('demoFiles/wrap1.png')),
                GUI.Button(topF, GO.PLBOTTOM, next(rainbow), 'Text',   func=lambda: customImg('demoFiles/wrap2.png')),
                GUI.Button(topF, GO.PLBOTTOM, next(rainbow), 'Planet', func=lambda: customImg('demoFiles/wrap3.png')),
            ])

            topF['Main'].append(GUI.Static(topF, GO.PCCENTER, pygame.Surface((0, 0))))

            def resetBotSur():
                botF['Main'][-1].set(pygame.Surface((0, 0)))
                G.Container.segs = []
                G.Container.cursegidx = None

            botF['Main'].extend([
                GUI.Empty(botF, GO.PCTOP, (0, 30)),
                GUI.Text(botF, GO.PCTOP, 'OUTPUT IMAGE', font=GO.FTITLE),

                GUI.Button(botF, GO.PRTOP, GO.CORANGE, 'Reset', func=resetBotSur)
            ])

            CCENTER = GO.PNEW((0.5, 0.5), (1, 0), (True, True))
            botF['Main'].append(GUI.Static(botF, CCENTER, pygame.Surface((0, 0))))

            makeSur()
        elif event == GO.EEVENT and element.type == pygame.KEYDOWN and element.key == pygame.K_r:
            G.Container.cursegidx = None
            G.Container.segs = []
        elif event == GO.ETICK:
            if G.Container.topF['Main'][1].active or G.Container.topF['Main'][3].active or \
               G.Container.topF['Main'][5].active or G.Container.topF['Main'][7].active:
                makeSur()
            
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                w = G.Container.topF['Main'][-1].get().get_width()
                pos = pygame.mouse.get_pos()[0]-(G.size[0]-w)/2
                pos = max(min(pos, w), 0)
                if G.Container.cursegidx is None:
                    G.Container.cursegidx = len(G.Container.segs)
                    G.Container.segs.append([pos, pos])
                else:
                    curSeg = G.Container.segs[G.Container.cursegidx]
                    if pos < curSeg[0]:
                        curSeg[0] = pos
                    if pos > curSeg[1]:
                        curSeg[1] = pos
            else:
                G.Container.cursegidx = None
        elif event == GO.EDRAW:
            w = G.Container.topF['Main'][-1].get().get_width()
            off = (G.size[0]-w)/2
            for seg in G.Container.segs:
                pygame.draw.line(G.WIN, (125, 125, 125), (seg[0]+off, 90), (seg[1]+off, 90), 5)
        elif event == GO.EELEMENTCLICK:
            if element == G.Container.GObtn:
                @G.Loading
                def load(slf):
                    import time
                    time.sleep(0.5)
                    pygame.event.pump()
                    off = G.Container.offset
                    topF = G.Container.topF['Main']

                    conns = []
                    for seg in G.Container.segs:
                        conns.append(Segment(seg[0], seg[1]))

                    slf.surf = wrapSurface(topF[-1].get(), topF[off+1].get(), pg2=False, constraints=conns)

                    slf.surf = pygame.transform.scale(slf.surf, (500, 500))
                fin, outslf = load()
                if fin:
                    G.Container.botF['Main'][-1].set(outslf.surf)
    
    screen()

# GENERATION STUFF

def TWorldsDemo():
    from BlazeSudio.utils import World
    World('test', 'Test World', 'A world for testing random stuff', 5, 100, override=True, callback=print)

def TTerrainGenDemo():
    from random import randint
    from BlazeSudio.utils import MapGen
    size = 500 # 1500
    n = 256
    inp = input('Input nothing to use random seed, input "." to use a preset good seed, or input your own INTEGER seed > ')
    if inp == '':
        map_seed = randint(0, 999999)
    elif inp == '.':
        map_seed = 762345
    else:
        map_seed = int(inp)
    useall = input('Type anything here to show all steps in terrain generation, or leave this blank and press enter to just show the finished product. > ') != ''
    m = MapGen()
    for txt in m.generate(size, map_seed, n, useall=useall, showAtEnd=True):
        print(txt)
    outs, trees = m.outs
    print(outs[0])
    pass

if __name__ == '__main__':
    try:
        import tkinter as Tk
        has_tk = True
        root = Tk.Tk()
    except ImportError:
        print("You don't have tkinter installed. Using the command line instead.\n")
        has_tk = False
    
    cmds = []

    def label(text):
        if has_tk:
            Tk.Label(root, text=text).pack()
        else:
            print('\n'+text)

    def button(text, command, requires_tk=False):
        def cmd(cmdd):
            if has_tk:
                root.destroy()
            print('loading demo %s...'%text)
            cmdd()
        if has_tk:
            Tk.Button(root, text=text, command=lambda: cmd(command)).pack()
        else:
            rtk = '*' if requires_tk else ''
            print(f'{len(cmds)}: {rtk}{text}')
            cmds.append(command)
    
    label('Node generator [image]:')
    button('Node Editor Demo',           NodeEditorDemo,                   )

    label('Graphics [graphics] / [game]:')
    button('Graphics Demo',              GraphicsDemo,                     )
    button('Lorem Ipsum Graphics Demo',  LoremGraphicsDemo,                )
    button('Theme Playground Demo',      ThemePgDemo,                  True)

    # TODO: Sound editor demo
    label('Collisions [collisions]:')
    button('Collisions Demo',            CollisionsDemo,                   )
    button('DEBUG Collisions Demo',      lambda: CollisionsDemo(True),     )

    # Broken generation stuff
    #button('Generate World Demo',        TWorldsDemo,                       )
    #button('Generate Terrain Demo',      TTerrainGenDemo,                   )


    label('Misc stuff:')
    button('Wrap Demo [game]',            WrapDemo,                        )
    button('Wrap Basic Demo [game]',      WrapBasicDemo,                   )
    
    if has_tk:
        root.after(1, lambda: root.attributes('-topmost', True))
        root.mainloop()
    else:
        print("*Requires TKinter")
        try:
            cmds[int(input('Enter the number of the demo you want to run > '))]()
        except ValueError:
            print('You entered an invalid number. Exiting...')
        except IndexError:
            print('You entered a number that is not in the list. Exiting...')
