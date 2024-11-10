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
    import BlazeSudio.graphics.options as GO
    from BlazeSudio.graphics import Graphic, GUI
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
            G['texts'].append(GUI.Text(G, GO.PCCENTER, 'Sorry, I meant a cool TEST', GO.CRED))
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
            L.grid = [
                [GUI.Text(L, L.LP, 'HI'), GUI.Text(L, L.LP, 'HELLO'), GUI.Text(L, L.LP, 'BYE')],
                [GUI.Text(L, L.LP, 'HEHE'), GUI.Text(L, L.LP, 'YES'), GUI.Text(L, L.LP, 'NO')],
                [GUI.Text(L, L.LP, 'HAVE'), GUI.Text(L, L.LP, 'A'), GUI.Text(L, L.LP, 'NICEDAY')],
                [None, GUI.Button(L, L.LP, GO.CORANGE, 'Hello!'), None]
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
                    pop = GUI.PopupFrame(G, GO.PCCENTER, (300, 250))
                    pop.layers[0].add('Alls')
                    pop['Alls'].extend([
                        GUI.Text(pop, GO.PCTOP, 'Popup', font=GO.FTITLE),
                        GUI.Text(pop, GO.PCCENTER, 'This is an example of a popup!', allowed_width=250),
                        GUI.Button(pop, GO.PRTOP, GO.CYELLOW, '❌', func=lambda: pop.remove()),
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

def MThemePgDemo():
    import themePlayground

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
