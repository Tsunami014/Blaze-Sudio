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
    NodeEditor(f)()

def GraphicsDemo():
    import BlazeSudio.graphics.options as GO
    from BlazeSudio.graphics import Screen, Loading, Progressbar, GUI
    from BlazeSudio.graphics.base import HiddenStatus
    from BlazeSudio.graphics.base import ReturnState
    import pygame
    from time import sleep
    @Loading.decor
    def test_loading(slf):
        slf['i'] = 0
        for slf['i'] in range(10):
            sleep(1)
    
    @Progressbar.decor(10)
    def test_loading2(slf):
        yield '0'
        slf['i'] = 0
        for slf['i'] in range(10):
            sleep(1)
            yield slf['i']+1
    
    class Test(Screen):
        def __init__(self, txt):
            super().__init__(GO.CWHITE)
            self.txt = txt
        
        def _LoadUI(self): # Load the graphics in!
            CTOP = GO.PNEW((0.5, 0), (1, 0), (True, False)) # Bcos usually the Center Top makes the elements stack down, so I make a new thing that stacks sideways
            LBOT = GO.PNEW((0, 1), (0, -1)) # Going up instead of right
            RTOP = GO.PNEW((1, 0), (-1, 0)) # Going left instead of down
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
            # I also showcase below many ways of doing the same things.
            tb = GUI.DebugTerminal(jump_to_shortcut=pygame.K_F5)
            for word in ['hi', 'bye', 'hello', 'goodbye', 'greetings', 'farewell']:
                f = lambda *args, word=word: self['events'].append(GUI.Toast(  # noqa: E731
                    f'{word[0].upper()}{word[1:]}{" " if len(args) > 0 else ""}{", ".join(args[:-1])}{" & " if len(args) > 1 else ""}{args[-1]}!'
                ))
                f.__doc__ = f"{word} *<str> : Says {word} with the given arguments"
                tb.addCmd(word, f)
            self['TB'].append(tb)

            f = GUI.ScaledByFrame(GO.PRBOTTOM, (500, 400))
            self['speshs'].append(f)
            f.layers[0].add('Alls')
            f['Alls'].extend([
                GUI.Text(GO.PLTOP, 'Scaled Frame', GO.CBLUE),
                GUI.Empty(GO.PLTOP, (0, 15)),
                GUI.Text(GO.PLTOP, 'Change scale:', GO.CGREEN),
                (cs := GUI.NumInputBox(GO.PLTOP, 100, GO.RHEIGHT, empty=2, minim=1, placeholdOnNum=None, decimals=True))
            ])
            self.changeScale = cs

            self['texts'].extend([
                GUI.Text(GO.PCCENTER, 'This is a cool thing', GO.CBLUE),
                (ivt := GUI.Text(GO.PCCENTER, '*Sorry*, I meant a cool *TEST*', GO.CRED)),
                (txt := GUI.Text(GO.PCCENTER, self.txt, GO.CGREEN))
            ])
            self.Invisi_T = ivt
            self.txt = txt

            self.inp = GUI.InputBox(GO.PCCENTER, 500, GO.RHEIGHT)
            self['endElms'].append(self.inp)
            self['space'].append(GUI.Empty(GO.PCCENTER, (0, 50)))
            self['endElms'].append(GUI.NumInputBox(GO.PCCENTER, 100, minim=-255, maxim=255, placeholdOnNum=None))
            self['endElms'].append(GUI.NumInputBox(GO.PCCENTER, 100, minim=-255, maxim=255, placeholder='Type decimal here!', empty=100, decimals=3))
            self['space'].append(GUI.Empty(GO.PCCENTER, (0, 50)))
            self['endElms'].append(GUI.DropdownButton(GO.PCCENTER, ['HI', 'BYE']))

            self['space'].append(GUI.Empty(LBOT, (0, 20)))
            self['buttons'].append(GUI.Button(LBOT, GO.CYELLOW, 'Button 1 :D'))
            self['texts'].append(GUI.Text(LBOT, 'Buttons above [^] and below [v]', GO.CBLUE))
            self.PopupBtn = GUI.Button(LBOT, GO.CMAUVE, 'Popup test')
            self.TextboxBtn = GUI.Button(LBOT, GO.CBLUE, 'Textbox test')
            self.LoadingBtn = GUI.Button(LBOT, GO.CGREEN, 'Loading test')
            self.LoadingBtn2 = GUI.Button(LBOT, GO.CGREY, 'Progressbar loading test')
            self.exitbtn = GUI.Button(GO.PLCENTER, GO.CRED, 'EXIT', GO.CWHITE, func=lambda: self.Abort())
            self['buttons'].extend([
                self.PopupBtn,
                self.TextboxBtn,
                self.LoadingBtn,
                self.LoadingBtn2,
                self.exitbtn
            ])

            self['texts'].extend([
                GUI.Text(CTOP, 'Are you '),
                GUI.Text(CTOP, 'happy? ', GO.CGREEN),
                GUI.Text(CTOP, 'Or sad?', GO.CRED)
            ])

            self.switches = [
                GUI.Switch(RTOP, 40, 2),
                GUI.Switch(RTOP, default=True),
            ]
            self['endElms'].extend(self.switches)
            self.colour = GUI.ColourPickerBTN(RTOP)
            self['endElms'].extend([
                self.colour,
                GUI.Empty(RTOP, (10, 10)),
                (mdInp := GUI.InputBox(RTOP, 600, GO.RHEIGHT, placeholder='Type in Markdown!'))
            ])
            mdInp.useMD = True

            L = GUI.GridLayout(GO.PCBOTTOM, outline=5)
            self['speshs'].append(L)
            L.grid = [
                [GUI.Text(L.LP, '**HI**'), None, GUI.Text(L.LP, '*BYE*')],
                [GUI.Text(L.LP, '***YES***'), GUI.Checkbox(L.LP), GUI.Text(L.LP, 'NO')],
                [GUI.Checkbox(L.LP, 20, check_size=10), GUI.Checkbox(L.LP, thickness=2), GUI.Checkbox(L.LP, check_size=40)],
                [GUI.Button(L.LP, GO.CORANGE, '*Hel-**looo!!***'), None, (sw := GUI.Switch(L.LP))]
            ]
            self.sw = sw

            TOPLEFT = GO.PSTATIC(10, 10) # Set a custom coordinate that never changes
            S = GUI.ScrollableFrame(TOPLEFT, (250, 200), (400, 450))
            self['speshs'].append(S)
            # This is another way of setting out your Stuff; having everything under one name.
            S.layers[0].add('Alls')
            S['Alls'].extend([
                GUI.Empty(GO.PCTOP, (0, 10)),
                GUI.Text(GO.PCTOP, 'Scroll me!', GO.CBLUE),
                GUI.Empty(GO.PCTOP, (0, 50)),
                GUI.InputBox(GO.PCTOP, 200, GO.RHEIGHT, weight=GO.SWLEFT),
                GUI.Empty(GO.PCTOP, (0, 50)),
                GUI.Button(GO.PCTOP, GO.CGREEN, 'Press me!', func=lambda: self.txt.set('### You pressed the button in the Scrollable :)')),
                GUI.Empty(GO.PCTOP, (0, 50)),
                GUI.Text(GO.PCTOP, 'Auto adjust scrollable height', GO.CORANGE, allowed_width=200),
                GUI.Switch(GO.PCTOP, speed=0.5)
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
                    self.txt.set('Ran for %i seconds%s' % (ret['i']+1, (' **Successfully!** :)' if succeeded else ' And *failed* :(')))
                elif obj == self.LoadingBtn2:
                    succeeded, ret = test_loading2()
                    self.txt.set('Ran for %i seconds%s' % (ret['i']+1, (' **Successfully!** :)' if succeeded else ' And *failed* :(')))
                elif obj == self.TextboxBtn:
                    bot = GO.PNEW((0.5, 1), (0, 0), (True, False))
                    dialog_box = GUI.TextBoxAdv(bot, text='HALOOO!!')
                    dialog_box.set_indicator()
                    dialog_box.set_portrait()
                    self['events'].append(dialog_box)
                    self.idx = 0
                elif obj == self.PopupBtn:
                    pop = GUI.PopupFrame(GO.PCCENTER, (350, 300))
                    pop.layers[0].add('Alls')
                    def rmpop(pop):
                        pop.remove()
                        return ReturnState.DONTCALL
                    pop['Alls'].extend([
                        GUI.Empty(GO.PCTOP, (0, 10)),
                        GUI.Text(GO.PCTOP, '# Popup'),
                        GUI.Text(GO.PCCENTER, 'This is an **example** of a popup!', allowed_width=250),
                        GUI.Button(GO.PRTOP, GO.CYELLOW, '❌', func=lambda p=pop: rmpop(p)),
                        GUI.Empty(GO.PCBOTTOM, (0, 10)),
                        GUI.InputBox(GO.PCBOTTOM, 250, GO.RNONE, 'Example textbox', maxim=16),
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
                    self['events'].append(GUI.Toast('Saved! (Don\'t worry - this does nothing)', GO.CGREEN))
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
    from BlazeSudio.graphics import Screen, RunInstantly, Loading, options as GO, GUI

    class Test(Screen, RunInstantly):
        def _LoadUI(self):
            self.layers[0].add('speshs')
            @Loading.decor
            def load(slf):
                S2 = GUI.ScrollableFrame(GO.PCCENTER, (900, 700), (2000, 11000))
                S2.layers[0].add('alls')
                with open('demoFiles/lorem.txt') as f:
                    lorem = f.read()
                S2['alls'].append(GUI.Text(GO.PCTOP, lorem, allowed_width=1900))
                self['speshs'].append(S2)
            fin, _ = load()
            if not fin:
                self.Abort()
    
    Test()

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
            polys = main.generateBounds(100, True, False, True)

            # Outer Polygon
            ps = list(polys[0])
            for p in ps:
                pygame.draw.circle(win, (125, 125, 125), p, 3)
            for i in range(len(ps)-1):
                pygame.draw.line(win, (125, 125, 125), ps[i], ps[i+1], 3)
            
            # Inner Shapes[Line]
            for i in polys[2]:
                pygame.draw.line(win, (125, 125, 125), i[0], i[1], 3)
                for j in i:
                    pygame.draw.circle(win, (125, 125, 125), j, 2)

        pygame.display.update()

def WrapDemo():
    from BlazeSudio.graphics import Screen, Progressbar, options as GO, GUI
    from BlazeSudio.utils.wrap import wrapSurface, Segment
    import pygame
    
    class Main(Screen):
        def __init__(self):
            super().__init__(GO.CGREY)
        
        def makeSur(self):
            topF = self.topF
            news = pygame.Surface((1, 2))
            news.set_at((0, 0), topF['Main'][1].get())
            news.set_at((0, 1), topF['Main'][3].get())
            news2 = pygame.transform.smoothscale(news, (topF['Main'][5].get(), topF['Main'][7].get()))
            self.inputSur = news2
            topF['Main'][-1].set(news2)
            self.segs = []
            self.cursegidx = None
        
        def _LoadUI(self):
            self.layers[0].add('Main')
            self.layers[1].add('Top')
            self.segs = []
            self.cursegidx = None
            topF = GUI.BaseFrame(self, GO.PCTOP, (self.size[0], self.size[1]//2), 2)
            topF.layers[0].add('Main')
            self.topF = topF
            botF = GUI.BaseFrame(self, GO.PCTOP, (self.size[0], self.size[1]//2), 2)
            botF.layers[0].add('Main')
            self.botF = botF

            self['Main'].extend([topF, botF])

            self.GObtn = GUI.Button(self, GO.PCCENTER, GO.CORANGE, 'Wrap!')
            self['Top'].append(self.GObtn)

            LTOP = GO.PNEW((0, 0), (0, 1))
            topF['Main'].extend([
                GUI.Text(topF, LTOP, 'Colour 1'),
                GUI.ColourPickerBTN(topF, LTOP),
                GUI.Text(topF, LTOP, 'Colour 2'),
                GUI.ColourPickerBTN(topF, LTOP, default=(10,255,50)),
                GUI.Text(topF, LTOP, 'Width'),
                GUI.NumInputBox(topF, LTOP, 100, GO.RHEIGHT, start=500, minim=1, maxim=1500, placeholdOnNum=None),
                GUI.Text(topF, LTOP, 'Height'),
                GUI.NumInputBox(topF, LTOP, 100, GO.RHEIGHT, start=100, minim=1, maxim=500, placeholdOnNum=None),
            ])

            RTOP = GO.PNEW((1, 0), (0, 1))
            self.offset = len(topF['Main'])
            topF['Main'].extend([
                GUI.Text(topF, RTOP, 'Top'),
                GUI.NumInputBox(topF, RTOP, 100, GO.RHEIGHT, empty=0.5, start=None, minim=0, maxim=2, placeholdOnNum=None, decimals=8),
                GUI.Text(topF, RTOP, 'Bottom'),
                GUI.NumInputBox(topF, RTOP, 100, GO.RHEIGHT, empty=-0.5, start=None, minim=-1, maxim=0, placeholdOnNum=None, decimals=8),
                GUI.Text(topF, RTOP, 'Limit'),
                GUI.Switch(topF, RTOP, default=True),
            ])

            topF['Main'].append(GUI.Text(topF, GO.PCTOP, '# INPUT IMAGE'))

            def customImg(img):
                topF['Main'][-1].set(pygame.image.load(img))
                self.segs = []
                self.cursegidx = None

            rainbow = GO.CRAINBOW()
            topF['Main'].extend([
                GUI.Button(topF, GO.PLBOTTOM, next(rainbow), 'Iris',   func=lambda: customImg('demoFiles/wrap1.png')),
                GUI.Button(topF, GO.PLBOTTOM, next(rainbow), 'Text',   func=lambda: customImg('demoFiles/wrap2.png')),
                GUI.Button(topF, GO.PLBOTTOM, next(rainbow), 'Planet', func=lambda: customImg('demoFiles/wrap3.png')),
            ])

            topF['Main'].append(GUI.Static(topF, GO.PCCENTER, pygame.Surface((0, 0))))

            def resetBotSur():
                botF['Main'][-1].set(pygame.Surface((0, 0)))
                self.segs = []
                self.cursegidx = None

            botF['Main'].extend([
                GUI.Empty(botF, GO.PCTOP, (0, 30)),
                GUI.Text(botF, GO.PCTOP, '# OUTPUT IMAGE'),

                GUI.Button(botF, GO.PRTOP, GO.CORANGE, 'Reset', func=resetBotSur)
            ])

            CCENTER = GO.PNEW((0.5, 0.5), (1, 0), (True, True))
            botF['Main'].append(GUI.ImageViewer(botF, CCENTER, pygame.Surface((0, 0)), (800, 400)))

            self.makeSur()
        
        def _Event(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.cursegidx = None
                    self.segs = []
                elif event.key == pygame.K_RETURN:
                    self.wrap()
        
        def _Tick(self):
            if self.topF['Main'][1].active or self.topF['Main'][3].active or \
               self.topF['Main'][5].active or self.topF['Main'][7].active:
                self.makeSur()
            
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                w = self.topF['Main'][-1].get().get_width()
                pos = pygame.mouse.get_pos()[0]-(self.size[0]-w)/2
                pos = max(min(pos, w), 0)
                if self.cursegidx is None:
                    self.cursegidx = len(self.segs)
                    self.segs.append([pos, pos])
                else:
                    curSeg = self.segs[self.cursegidx]
                    if pos < curSeg[0]:
                        curSeg[0] = pos
                    if pos > curSeg[1]:
                        curSeg[1] = pos
            else:
                self.cursegidx = None
        
        def _DrawAft(self):
            w = self.topF['Main'][-1].get().get_width()
            off = (self.size[0]-w)/2
            for seg in self.segs:
                pygame.draw.line(self.WIN, (125, 125, 125), (seg[0]+off, 90), (seg[1]+off, 90), 5)
        
        def _ElementClick(self, obj):
            if obj == self.GObtn:
                self.wrap()
        
        def wrap(self):
            @Progressbar.decor(4)
            def load(slf):
                import time
                time.sleep(0.5)
                pygame.event.pump()
                yield 'Setting up'
                off = self.offset
                topF = self.topF['Main']

                conns = []
                for seg in self.segs:
                    conns.append(Segment(seg[0], seg[1]))

                slf['surf'] = yield from wrapSurface(
                    topF[-1].get(), 
                    topF[off+1].get(), 
                    topF[off+3].get(), 
                    topF[off+5].get(), 
                    pg2=False, 
                    constraints=conns, 
                    isIter=True
                )

                yield 'Finishing up'
            fin, outs = load()
            if fin:
                self.botF['Main'][-1].set(outs['surf'])
    
    Main()()

def TsetCollDemo():
    from BlazeSudio.graphics import Screen, Loading, options as GO, GUI
    from BlazeSudio.utils import genCollisions as gen
    from functools import partial
    import pygame
    
    tset = pygame.image.load('demoFiles/sampleTileset.png')

    class Main(Screen):
        def getTile(self, idx):
            if idx is None:
                return
            self.poly = None
            self.tile = tset.subsurface((idx*32, 0, 32, 32))
        
        @Loading.decor
        def calcPoly(slf, self):
            chosen = self.opts.index(self.chooser.get())
            if chosen == 0:
                self.poly = None
            elif chosen == 1:
                self.poly = [(0, 0), (32, 0), (32, 32), (0, 32)]
            elif chosen == 2:
                self.poly = gen.bounding_box(self.tile)
            elif chosen == 3:
                self.poly = gen.corners(self.tile)
            elif chosen == 4:
                self.poly = gen.approximate_polygon(self.tile)
        
        def __init__(self):
            self.getTile(0)
            self.opts = [
                'No collisions', 
                'Cover entire shape',
                'Bounding box', 
                'Corners',
                'Trace shape'
            ]
            super().__init__()

        def _Event(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.calcPoly(self)
        
        def _LoadUI(self):
            self.layers[0].add('Main')

            PCTOP = GO.PNEW((0.5, 0), (1, 0), (True, False))
            self.scale = GUI.NumInputBox(PCTOP, 100, GO.RNONE, start=None, empty=10, minim=1, maxim=30, placeholder='Scale by size', decimals=2)
            chooser = GUI.DropdownButton(PCTOP, ['Tile %i'%i for i in range(tset.get_width()//32)], func=lambda i: self.getTile(i))
            self.chooser = GUI.DropdownButton(PCTOP, self.opts)

            goBtn = GUI.Button(GO.PCBOTTOM, GO.CGREEN, 'Go!', func=partial(self.calcPoly, self))

            self['Main'].extend([
                self.scale,
                chooser,
                self.chooser,
                goBtn
            ])
        
        def _Tick(self):
            scale = self.scale.get()

            def outPos(x, y):
                center_x = (self.size[0] - 32 * scale) / 2
                center_y = (self.size[1] - 32 * scale) / 2
                return (x * scale + center_x, y * scale + center_y)
            
            self.WIN.blit(pygame.transform.scale(self.tile, (32*scale, 32*scale)), outPos(0, 0))

            if self.poly is not None:
                pygame.draw.polygon(self.WIN, (125, 125, 125), [outPos(*p) for p in self.poly], 4)
    
    Main()()

def SoundDemo():
    from BlazeSudio.graphics import Screen, GUI
    import BlazeSudio.graphics.options as GO
    from BlazeSudio.Game.sound import Beep
    from pygame.locals import KEYDOWN, K_RETURN
    class Main(Screen):
        def _LoadUI(self):
            self.layers[0].add_many(['Main', 'go'])
            fs = {
                'Sin': Beep.sin,
                'Square': Beep.square,
                'Triangle': Beep.triangle,
                'Noise': Beep.noise
            }
            self['Main'].extend([
                GUI.Text(GO.PCTOP, '# Sounds demo'),
                GUI.Text(GO.PLCENTER, '## OPTIONS'),
                GUI.Text(GO.PLCENTER, 'Type of wave'),
                (typ := GUI.DropdownButton(GO.PLCENTER, list(fs.keys()))),
                GUI.Text(GO.PLCENTER, 'Frequency left'),
                (Lfreq := GUI.NumInputBox(GO.PLCENTER, 100, GO.RNONE, minim=1, empty=500, placeholdOnNum=None)),
                GUI.Text(GO.PLCENTER, 'Frequency right'),
                (Rfreq := GUI.NumInputBox(GO.PLCENTER, 100, GO.RNONE, minim=0, empty=0, placeholdOnNum=0, placeholder='Left')),
            ])
            self['go'].append(GUI.Button(GO.PCCENTER, GO.CORANGE, 'Beep', func=lambda: fs[typ.get()](Lfreq.get(), Rfreq.get() or None)))
        
        def _Event(self, event):
            if event.type == KEYDOWN and event.key == K_RETURN:
                self['go'][0].func()
    
    Main()()

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
    button('Node Editor Demo',              NodeEditorDemo,                   )

    label('Graphics [graphics] / [game]:')
    button('Graphics Demo',                 GraphicsDemo,                     )
    button('Lorem Ipsum Graphics Demo',     LoremGraphicsDemo,                )
    button('Theme Playground Demo',         ThemePgDemo,                  True)

    # TODO: Sound editor demo
    label('Collisions [collisions]:')
    button('Collisions Demo',               CollisionsDemo,                   )
    button('DEBUG Collisions Demo',         lambda: CollisionsDemo(True),     )

    label('Wrapping [game]:')
    button('Wrap Demo',                     WrapDemo,                         )
    button('Wrap Basic Demo',               WrapBasicDemo,                    )

    label('Misc stuff:')
    button('Tileset Collision Demo [game]', TsetCollDemo,                     )
    button('Sound Demo [game]',             SoundDemo,                        )
    
    if has_tk:
        root.after(1, lambda: root.attributes('-topmost', True))
        root.mainloop()
    else:
        print("*Requires TKinter for the demo")
        try:
            cmds[int(input('Enter the number of the demo you want to run > '))]()
        except ValueError:
            print('You entered an invalid number. Exiting...')
        except IndexError:
            print('You entered a number that is not in the list. Exiting...')
