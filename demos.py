# Main STUFF
import warnings

from BlazeSudio.graphics.GUI.base import ReturnState
from BlazeSudio.utils.wrap import makeShape
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
    from BlazeSudio.graphics import Graphic, GUI
    from BlazeSudio.graphics.GUI.base import HiddenStatus
    import pygame
    from time import sleep
    G = Graphic()
    @G.Loading
    def test_loading(self):
        for self.i in range(10):
            sleep(1)
    
    @G.Screen
    def test(event, txt, element=None, aborted=False): # You do not need args and kwargs if you KNOW that your function will not take them in. Include what you need.
        if event == GO.ELOADUI: # Load the graphics in!
            CTOP = GO.PNEW((0.5, 0), (1, 0), (True, False)) # Bcos usually the Center Top makes the elements stack down, so I make a new thing that stacks sideways
            LBOT = GO.PNEW((0, 1), (0, -1))
            G.Clear()
            G.layers[0].add_many([
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
            G['TB'].append(GUI.TerminalBar(G))

            f = GUI.ScaledByFrame(G, GO.PRBOTTOM, (500, 400))
            G['speshs'].append(f)
            f.layers[0].add('Alls')
            LTOP = GO.PNEW((0, 0), (0, 1))
            f['Alls'].extend([
                GUI.Text(f, LTOP, 'Scaled Frame', GO.CBLUE),
                GUI.Empty(f, LTOP, (0, 15)),
                GUI.Text(f, LTOP, 'Change scale:', GO.CGREEN),
            ])
            G.Container.changeScale = GUI.NumInputBox(f, LTOP, 100, GO.RHEIGHT, start=2, min=1, placeholdOnNum=None)
            f['Alls'].append(G.Container.changeScale)

            G['texts'].append(GUI.Text(G, GO.PCCENTER, 'This is a cool thing', GO.CBLUE))
            G.Container.Invisi_T = GUI.Text(G, GO.PCCENTER, 'Sorry, I meant a cool TEST', GO.CRED)
            G['texts'].append(G.Container.Invisi_T)
            G.Container.txt = GUI.Text(G, GO.PCCENTER, txt, GO.CGREEN)
            G['texts'].append(G.Container.txt)
            G.Container.inp = GUI.InputBox(G, GO.PCCENTER, 500, GO.RHEIGHT, font=GO.FFONT)
            G['endElms'].append(G.Container.inp)
            G['space'].append(GUI.Empty(G, GO.PCCENTER, (0, 50)))
            G['endElms'].append(GUI.NumInputBox(G, GO.PCCENTER, 100, font=GO.FFONT, min=-255, max=255))
            G['space'].append(GUI.Empty(G, GO.PCCENTER, (0, 50)))
            G['endElms'].append(GUI.DropdownButton(G, GO.PCCENTER, ['HI', 'BYE']))

            G['space'].append(GUI.Empty(G, LBOT, (0, 20)))
            G['buttons'].append(GUI.Button(G, LBOT, GO.CYELLOW, 'Button 1 :D'))
            G['texts'].append(GUI.Text(G, LBOT, 'Buttons above [^] and below [v]', GO.CBLUE))
            G.Container.PopupBtn = GUI.Button(G, LBOT, GO.CMAUVE, 'Popup test')
            G['buttons'].append(G.Container.PopupBtn)
            G.Container.TextboxBtn = GUI.Button(G, LBOT, GO.CBLUE, 'Textbox test')
            G['buttons'].append(G.Container.TextboxBtn)
            G.Container.LoadingBtn = GUI.Button(G, LBOT, GO.CGREEN, 'Loading test')
            G['buttons'].append(G.Container.LoadingBtn)
            G.Container.exitbtn = GUI.Button(G, GO.PLCENTER, GO.CRED, 'EXIT', GO.CWHITE, func=lambda: G.Abort())
            G['buttons'].append(G.Container.exitbtn)

            G['texts'].extend([
                GUI.Text(G, CTOP, 'Are you '),
                GUI.Text(G, CTOP, 'happy? ', GO.CGREEN),
                GUI.Text(G, CTOP, 'Or sad?', GO.CRED)
            ])

            G.Container.switches = [
                GUI.Switch(G, GO.PRTOP, 40, 2),
                GUI.Switch(G, GO.PRTOP, default=True),
            ]
            G['endElms'].extend(G.Container.switches)
            G.Container.colour = GUI.ColourPickerBTN(G, GO.PRTOP)
            G['endElms'].append(G.Container.colour)

            L = GUI.GridLayout(G, GO.PCBOTTOM, outline=5)
            G['speshs'].append(L)
            G.Container.sw = GUI.Switch(L, L.LP)
            L.grid = [
                [GUI.Text(L, L.LP, 'HI'), GUI.Text(L, L.LP, 'HELLO'), GUI.Text(L, L.LP, 'BYE')],
                [GUI.Text(L, L.LP, 'HEHE'), GUI.Text(L, L.LP, 'YES'), GUI.Text(L, L.LP, 'NO')],
                [GUI.Text(L, L.LP, 'HAVE'), GUI.Text(L, L.LP, 'A'), GUI.Text(L, L.LP, 'NICEDAY')],
                [GUI.Button(L, L.LP, GO.CORANGE, 'Hello!'), None, G.Container.sw]
            ]

            TOPLEFT = GO.PSTATIC(10, 10) # Set a custom coordinate that never changes
            S = GUI.ScrollableFrame(G, TOPLEFT, (250, 200), (400, 450))
            G['speshs'].append(S)
            # This is another way of setting out your Stuff; having everything under one name.
            S.layers[0].add('Alls')
            S['Alls'].extend([
                GUI.Empty(S, GO.PCTOP, (0, 10)),
                GUI.Text(S, GO.PCTOP, 'Scroll me!', GO.CBLUE),
                GUI.Empty(S, GO.PCTOP, (0, 50)),
                GUI.InputBox(S, GO.PCTOP, 200, GO.RHEIGHT, weight=GO.SWLEFT),
                GUI.Empty(S, GO.PCTOP, (0, 50)),
                GUI.Button(S, GO.PCTOP, GO.CGREEN, 'Press me!', func=lambda: G.Container.txt.set('You pressed the button in the Scrollable :)')),
                GUI.Empty(S, GO.PCTOP, (0, 50)),
                GUI.Text(S, GO.PCTOP, 'Auto adjust scrollable height', GO.CORANGE, allowed_width=200),
                GUI.Switch(S, GO.PCTOP, speed=0.5)
            ])
        elif event == GO.ETICK: # This runs every 1/60 secs (each tick)
            # Return False if you want to quit the screen. This is not needed if you never want to do this.
            G['speshs'][0].scale = G.Container.changeScale.get()
            S = G['speshs'][2]
            e = S['Alls'][-1]
            if e.get():
                S.sizeOfScreen = (S.sizeOfScreen[0], e.stackP()[1]+e.size[1]+30)
            else:
                S.sizeOfScreen = (S.sizeOfScreen[0], 450)
        elif event == GO.EELEMENTCLICK: # Some UI element got clicked!
            if element.type == GO.TBUTTON:
                # This gets passed 'element': the element that got clicked.
                if element == G.Container.LoadingBtn:
                    succeeded, ret = test_loading()
                    G.Container.txt.set('Ran for %i seconds%s' % (ret.i+1, (' Successfully! :)' if succeeded else ' And failed :(')))
                elif element == G.Container.TextboxBtn:
                    bot = GO.PNEW((0.5, 1), (0, 0), (True, False))
                    dialog_box = GUI.TextBoxAdv(G, bot, text='HALOOO!!')
                    dialog_box.set_indicator()
                    dialog_box.set_portrait()
                    G['events'].append(dialog_box)
                    G.Container.idx = 0
                elif element == G.Container.PopupBtn:
                    pop = GUI.PopupFrame(G, GO.PCCENTER, (350, 300))
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
                    G['events'].append(pop) # I know it's not an event, but o well.
                else:
                    G.Container.txt.set(element.txt) # put name of button in middle
            elif element.type == GO.TTEXTBOX:
                if G.Container.idx == 0:
                    element.set("Happy coding!")
                    G.Container.idx = 1
                else: 
                    element.remove()
            elif element.type == GO.TINPUTBOX:
                G.Container.txt.set(element.get().strip())
            elif element.type == GO.TSWITCH:
                if element == G.Container.sw:
                    if element.get():
                        G.Container.Invisi_T.hiddenStatus = HiddenStatus.GONE
                    else:
                        G.Container.Invisi_T.hiddenStatus = HiddenStatus.SHOWING
        elif event == GO.EEVENT: # When something like a mouse or keyboard button is pressed. Is passed 'element' too, but this time it is an event
            if element.type == pygame.KEYDOWN:
                if element.key == pygame.K_s and element.mod & pygame.KMOD_CTRL:
                    G['events'].append(GUI.Toast(G, 'Saved! (Don\'t worry - this does nothing)', GO.CGREEN))
            elif element.type == pygame.MOUSEBUTTONDOWN and element.button == pygame.BUTTON_RIGHT:
                opts = ['HI', 'BYE', 'HI AGAIN']
                def dropdownSelect(resp):
                    if isinstance(resp, int):
                        G.Container.txt.set(opts[resp])
                G['events'].append(GUI.Dropdown(G, pygame.mouse.get_pos(), opts, func=dropdownSelect))
        elif event == GO.ELAST:
            # This also gets passed 'aborted': Whether you aborted or exited the screen
            S = G['speshs'][2]
            return { # Whatever you return here will be returned by the function
                'Aborted?': aborted, 
                'endElms': G['endElms']+[
                    # These are the input and the switch
                    S['Alls'][3],
                    S['Alls'][-1],
                ]}
    
    print(test('Right click or press anything or press ctrl+s!'))
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
    import os
    if debug:
        os.environ['debug'] = 'True'
    from demoFiles import collisionsDemo  # noqa: F401

def WrapBasicDemo():
    from BlazeSudio.utils.wrap import constraints
    from BlazeSudio.collisions import Point
    import pygame
    pygame.init()

    win = pygame.display.set_mode()
    pygame.display.toggle_fullscreen()

    main = makeShape.MakeShape(100)

    conns = {
        '|': constraints.SpecificAngle(0),
        '-': constraints.SpecificAngle(90),
        '/': constraints.SpecificAngle(45),
        '\\': constraints.SpecificAngle(-45),
    }

    run = True
    heldSegment = None
    selectedSegment = None
    movingMode = False
    while run:
        newMM = pygame.key.get_mods() & pygame.KMOD_ALT
        if newMM and not movingMode:
            main.makeShape()
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
                                if val in main.segProps[selectedSegment[1]]:
                                    main.segProps[selectedSegment[1]].remove(val)
                                else:
                                    main.segProps[selectedSegment[1]].append(val)
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
            if main.segProps[i]:
                col = (10, 50, 255)
            else:
                col = (255, 255, 255)
            pygame.draw.line(win, col, segs[i][0], segs[i][1], 10)
        for j in main.joints:
            if j == selectedJoint[1]:
                pygame.draw.circle(win, (255, 100, 100), j, 5)
            else:
                pygame.draw.circle(win, (10, 50, 255), j, 5)
        
        if selectedSegment is not None:
            h = boxSze+gap*2
            w = (boxSze+gap)*boxes+gap
            x, y = (selectedSegment[0][0][0]+selectedSegment[0][1][0]-w)/2, min(selectedSegment[0][0][1], selectedSegment[0][1][1])-h-gap*3
            pygame.draw.rect(win, (125, 125, 125), (x, y, w, h), border_radius=4)
            vals = list(conns.values())
            f = pygame.font.Font(None, boxSze)
            for i in range(boxes):
                r = pygame.Rect(x+(boxSze+gap)*i+gap, y+gap, boxSze, boxSze)
                props = main.segProps[selectedSegment[1]]
                if vals[i] in props:
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

        pygame.display.update()

def WrapDemo():
    from BlazeSudio.graphics import Graphic, GO, GUI
    from BlazeSudio.utils.wrap import wrapSurface
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
    
    @G.Screen
    def screen(event, element=None, aborted=False):
        if event == GO.ELOADUI:
            G.Clear()
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

            topF['Main'].append(GUI.Static(topF, GO.PCCENTER, pygame.Surface((0, 0))))

            def resetBotSur():
                botF['Main'][-1].set(pygame.Surface((0, 0)))

            botF['Main'].extend([
                GUI.Empty(botF, GO.PCTOP, (0, 30)),
                GUI.Text(botF, GO.PCTOP, 'OUTPUT IMAGE', font=GO.FTITLE),

                GUI.Button(botF, GO.PRTOP, GO.CORANGE, 'Reset', func=resetBotSur)
            ])

            CCENTER = GO.PNEW((0.5, 0.5), (1, 0), (True, True))
            botF['Main'].append(GUI.Static(botF, CCENTER, pygame.Surface((0, 0))))

            makeSur()
        elif event == GO.ETICK:
            makeSur()
        elif event == GO.EELEMENTCLICK:
            if element == G.Container.GObtn:
                @G.Loading
                def load(slf):
                    import time
                    time.sleep(0.5)
                    pygame.event.pump()
                    off = G.Container.offset
                    topF = G.Container.topF['Main']
                    slf.surf = wrapSurface(topF[-1].get(), topF[off+1].get(), pg2=False)
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
