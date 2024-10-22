# Main STUFF

def MNodeEditorDemo():
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

def MGraphicsDemo():
    import pygame
    import BlazeSudio.graphics.options as GO
    from BlazeSudio.graphics import Graphic, GUI
    from time import sleep
    G = Graphic()
    @G.Loading
    def test_loading(self):
        for self.i in range(10):
            sleep(1)
    
    @G.Screen
    def test(event, txt, element=None, aborted=False): # You do not need args and kwargs if you KNOW that your function will not take them in. Include what you need.
        if event == GO.ELOADUI: # Load the graphics in!
            CTOP = GO.PNEW((1, 0), GO.PCTOP.func) # Bcos usually the Center Top makes the elements stack down, so I make a new thing that stacks sideways
            LBOT = GO.PNEW((0, -1), GO.PLBOTTOM.func)
            G.Clear()
            G.layers[0].add_many([
                # You can name these whatever you want, but I like to keep them the same as the type.
                'TB',
                'texts',
                'space',
                'buttons',
                'events',
                'scrolls',
                'endElms', # These will be the ones I find in the GO.ELAST event
            ])
            # I chose this because you can see the different sections of the screen, but you can do what you want; as long as they end up on the list it's ok.
            G['TB'].append(GUI.TerminalBar(G))

            G['texts'].extend([
                GUI.Text(G, GO.PRBOTTOM, 'HI', GO.CGREEN, GO.FTITLE),
                GUI.Text(G, GO.PRBOTTOM, ':)', GO.CBLACK, GO.FTITLE)
            ])

            G['space'].append(GUI.Empty(G, GO.PCCENTER, (0, -150))) # Yes, you can have negative space. This makes the next things shifted the other direction.
            G['texts'].append(GUI.Text(G, GO.PCCENTER, 'This is a cool thing', GO.CBLUE))
            G['texts'].append(GUI.Text(G, GO.PCCENTER, 'Sorry, I meant a cool TEST', GO.CRED))
            G.Container.txt = GUI.Text(G, GO.PCCENTER, txt, GO.CGREEN)
            G['texts'].append(G.Container.txt)
            G.Container.inp = GUI.InputBox(G, GO.PCCENTER, 200, font=GO.FFONT, maxim=16)
            G['endElms'].append(G.Container.inp)
            G['space'].append(GUI.Empty(G, GO.PCCENTER, (0, 50)))
            G['endElms'].append(GUI.NumInputBox(G, GO.PCCENTER, 100, font=GO.FFONT, min=-255, max=255))

            G['space'].append(GUI.Empty(G, LBOT, (0, 20)))
            G['buttons'].append(GUI.Button(G, LBOT, GO.CYELLOW, 'Button 1 :D'))
            G['texts'].append(GUI.Text(G, LBOT, 'Buttons above [^] and below [v]', GO.CBLUE))
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

            TOPLEFT = GO.PSTATIC(10, 10) # Set a custom coordinate that never changes
            S = GUI.ScrollableFrame(G, TOPLEFT, (250, 200), (250, 350))
            G['scrolls'].append(S)
            # This is another way of setting out your Stuff; having everything under one name.
            S.layers[0].add_many([
                'Alls'
            ])
            S['Alls'].extend([
                GUI.Empty(S, GO.PCTOP, (10, 20)),
                GUI.Text(S, GO.PCTOP, 'Scroll me!', GO.CBLUE),
                GUI.Empty(S, GO.PCTOP, (0, 50)),
                GUI.InputBox(S, GO.PCTOP, 100, GO.RHEIGHT),
                GUI.Empty(S, GO.PCTOP, (0, 50)),
                GUI.Button(S, GO.PCTOP, GO.CGREEN, 'Press me!', func=lambda: G.Container.txt.set('You pressed the button in the Scrollable :)')),
                GUI.Empty(S, GO.PCTOP, (0, 50)),
                GUI.Switch(S, GO.PCTOP, speed=0.5)
            ])
        elif event == GO.ETICK: # This runs every 1/60 secs (each tick)
            pass # Return False if you want to quit the screen. This is not needed if you never want to do this.
        elif event == GO.EELEMENTCLICK: # Some UI element got clicked!
            if element.type == GO.TBUTTON:
                # This gets passed 'element': the element that got clicked.
                if element == G.Container.LoadingBtn:
                    succeeded, ret = test_loading()
                    G.Container.txt.set('Ran for %i seconds%s' % (ret.i+1, (' Successfully! :)' if succeeded else ' And failed :(')))
                elif element == G.Container.TextboxBtn:
                    bot = GO.PNEW((0, 0), GO.PCBOTTOM.func, 1)
                    dialog_box = GUI.TextBoxAdv(G, bot, text='HALOOO!!')
                    dialog_box.set_indicator()
                    dialog_box.set_portrait()
                    G['events'].append(dialog_box)
                    G.Container.idx = 0
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
        elif event == GO.EEVENT: # When something like a mouse or keyboard button is pressed. Is passed 'element' too, but this time it is an event
            if element.type == pygame.KEYDOWN:
                if element.key == pygame.K_s and element.mod & pygame.KMOD_CTRL:
                    G['events'].append(GUI.Toast(G, 'Saved! (Don\'t worry - this does nothing)', GO.CGREEN))
            elif element.type == pygame.MOUSEBUTTONDOWN and element.button == pygame.BUTTON_RIGHT:
                opts = ['HI', 'BYE', 'HI AGAIN']
                resp = G.Dropdown(opts)
                if isinstance(resp, int):
                    G.Container.txt.set(opts[resp])
        elif event == GO.ELAST:
            # This also gets passed 'aborted': Whether you aborted or exited the screen
            S = G['scrolls'][0]
            return { # Whatever you return here will be returned by the function
                'Aborted?': aborted, 
                'endElms': G['endElms']+[
                    # These are the input and the switch
                    S['Alls'][3],
                    S['Alls'][-1],
                ]}
    
    print(test('Right click or press anything or press ctrl+s!'))
    pygame.quit() # this here for very fast quitting

def MThemePgDemo():
    try:
        from tkinter.filedialog import askopenfilename
    except ImportError as e:
        print('Sorry, this demo requires Tkinter and it could not be found.')
        raise e
    from BlazeSudio.graphics import Graphic, GUI, options as GO
    from BlazeSudio.graphics.GUI.base import ReturnState
    from threading import Thread
    G = Graphic()
    G.layers[0].add_many([
        'Main',
        'Left',
        'Right'
    ])

    def changeTheme(position, themePart):
        def change():
            def ask():
                newf = askopenfilename(filetypes=[('Image file', '*.png *.jpg *.jpeg *.bmp *.gif')])
                if newf:
                    setattr(GUI.GLOBALTHEME.THEME, themePart, GUI.Image(newf))
                    t1.set(newf)
            Thread(target=ask, daemon=True).start()
            return ReturnState.DONTCALL
        def unset():
            setattr(GUI.GLOBALTHEME.THEME, themePart, None)
            t1.set('None')
            return ReturnState.DONTCALL
        b1 = GUI.Button(G, position, GO.CORANGE, 'Change the image source 🔁', func=change, allowed_width=300)
        b2 = GUI.Button(G, position, GO.CRED, 'Unset the image source ❎', func=unset, allowed_width=300)
        n = getattr(GUI.GLOBALTHEME.THEME, themePart)
        if n is None:
            n = 'None'
        else:
            n = n.fname
        t1 = GUI.Text(G, position, n, allowed_width=300)
        return [
            b1,
            b2,
            t1
        ]

    @G.Screen
    def testButton(event, element=None, aborted=False):
        if event == GO.ELOADUI:
            G.Clear()
            G.Container.MainBtn = GUI.Button(G, GO.PCCENTER, GO.CRED, 'Hello!')
            G['Main'].append(G.Container.MainBtn)
            LTOP = GO.PNEW([0, 1], GO.PLTOP.func, 0, 0)
            G['Left'].extend([
                GUI.Text(G, LTOP, 'Sample button properties', font=GO.FTITLE),
                GUI.Text(G, LTOP, 'Colour of button'),
                GUI.ColourPickerBTN(G, LTOP),
                GUI.Text(G, LTOP, 'Colour of text'),
                GUI.ColourPickerBTN(G, LTOP, default=(0, 0, 0)),
                GUI.Text(G, LTOP, 'Text in button'),
                GUI.InputBox(G, LTOP, 100, GO.RHEIGHT, starting_text='Sample'),
                GUI.Text(G, LTOP, 'Allowed width'),
                GUI.NumInputBox(G, LTOP, 100, GO.RHEIGHT, start=0, min=0),
                GUI.Text(G, LTOP, 'On hover enlarge'),
                GUI.NumInputBox(G, LTOP, 100, GO.RHEIGHT, start=5, min=0),
                GUI.Text(G, LTOP, 'Spacing'),
                GUI.NumInputBox(G, LTOP, 100, GO.RHEIGHT, start=2, min=0),
            ])
            RTOP = GO.PNEW([0, 1], GO.PRTOP.func, 0, 0)
            G['Right'].extend([
                GUI.Text(G, RTOP, 'Button theme properties', font=GO.FTITLE),
                *changeTheme(RTOP, 'BUTTON')
            ])
        elif event == GO.ETICK:
            G.Container.MainBtn.cols = {'BG': G['Left'][2].get(), 'TXT': G['Left'][4].get()}
            G.Container.MainBtn.set(G['Left'][6].get(), allowed_width=(G['Left'][8].get() or None))
            G.Container.MainBtn.OHE = G['Left'][10].get()
            G.Container.MainBtn.spacing = G['Left'][12].get()
        # elif event == GO.EELEMENTCLICK:
        #     GUI.GLOBALTHEME.THEME.BUTTON = element.get()

    @G.Screen
    def test(event, element=None, aborted=False):
        if event == GO.ELOADUI:
            G.Clear()
            G['Main'].append(GUI.Text(G, GO.PCTOP, 'THEME EDITOR', font=GO.FTITLE))
            rainbow = GO.CRAINBOW()
            G['Main'].extend([
                GUI.Button(G, GO.PLTOP, next(rainbow), 'Test button', func=testButton),
            ])

    test()

def MCollisionsDemo(debug=False):
    import os
    if debug:
        os.environ['debug'] = 'True'
    from demoFiles import collisionsDemo  # noqa: F401

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

    def button(text, command):
        def cmd(cmdd):
            if has_tk:
                root.destroy()
            print('loading demo %s...'%text)
            cmdd()
        if has_tk:
            Tk.Button(root, text=text, command=lambda: cmd(command)).pack()
        else:
            print(f'{len(cmds)}: {text}')
            cmds.append(command)
    
    label('Main stuff:') # Nodes
    button('Node Editor Demo',           MNodeEditorDemo              )
    button('Graphics Demo',              MGraphicsDemo                )
    button('Theme Playground Demo',      MThemePgDemo                 )
    # TODO: Sound editor demo
    button('Collisions Demo',            MCollisionsDemo              )
    button('DEBUG Collisions Demo',      lambda: MCollisionsDemo(True))

    label('Generation stuff:') # Terrain
    button('Generate World Demo',        TWorldsDemo                  )
    button('Generate Terrain Demo',      TTerrainGenDemo              )
    
    if has_tk:
        root.after(1, lambda: root.attributes('-topmost', True))
        root.mainloop()
    else:
        try:
            cmds[int(input('Enter the number of the demo you want to run > '))]()
        except ValueError:
            print('You entered an invalid number. Exiting...')
        except IndexError:
            print('You entered a number that is not in the list. Exiting...')
