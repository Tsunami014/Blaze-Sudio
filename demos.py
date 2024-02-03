def GraphicsDemo():
    import pygame
    import graphics.graphics_options as GO
    from graphics import Graphic
    from time import sleep
    t = input('Please input the starting text for the middle: ')
    G = Graphic()
    @G.Loading
    def test_loading(self):
        for self.i in range(10):
            sleep(1)
    
    @G.Graphic
    def test(event, txt, element=None, aborted=False): # You do not need args and kwargs if you KNOW that your function will not take them in. Include what you need.
        if event == GO.EFIRST: # First, before anything else happens in the function
            G.Container.txt = txt
        if event == GO.ELOADUI: # Load the graphics
            CTOP = GO.PNEW([1, 0], GO.PSTACKS[GO.PCTOP][1]) # Bcos usually the Center Top makes the elements stack down, so I make a new thing that stacks sideways
            LBOT = GO.PNEW([0, -1], GO.PSTACKS[GO.PLBOTTOM][1])
            try:
                prevs = [G.uids[i].get() for i in (G.Container.switches+[G.Container.numinp,G.Container.inp])] + [G.uids[G.Container.colour].picker.p]
                prevTG = [G.uids[G.Container.scrollable].G.uids[G.Container.otherswitch].get(), G.uids[G.Container.scrollable].scroll]
            except:
                prevs = [False, False, 0, '', (0, 0.5)]
                prevTG = [False, 0]
            G.Clear()
            G.add_text('HI', GO.CGREEN, GO.PRBOTTOM, GO.FTITLE)
            G.add_text(':) ', GO.CBLACK, GO.PRBOTTOM, GO.FTITLE)
            G.add_empty_space(GO.PCCENTER, 0, -150) # Yes, you can have negative space. This makes the next things shifted the other direction.
            G.add_text('This is a cool thing', GO.CBLUE, GO.PCCENTER)
            G.add_text('Sorry, I meant a cool TEST', GO.CRED, GO.PCCENTER)
            G.add_text(G.Container.txt, GO.CGREEN, GO.PCCENTER)
            G.add_empty_space(LBOT, 0, 20)
            G.add_button('Button 1 :D', GO.CYELLOW, LBOT)
            G.add_text('Buttons above [^] and below [v]', GO.CBLUE, LBOT)
            G.add_button('Textbox test', GO.CBLUE, LBOT)
            G.add_button('Loading test', GO.CGREEN, LBOT)
            G.Container.exitbtn = G.add_button('EXIT', GO.CRED, GO.PLCENTER)
            G.add_empty_space(CTOP, -150, 0) # Center it a little more
            G.add_text('Are you ', GO.CBLACK, CTOP)
            G.add_text('happy? ', GO.CGREEN, CTOP)
            G.add_text('Or sad?', GO.CRED, CTOP)
            G.Container.inp = G.add_input(GO.PCCENTER, GO.FFONT, maximum=16, start=prevs[3])
            G.add_empty_space(GO.PCCENTER, 0, 50)
            G.Container.numinp = G.add_num_input(GO.PCCENTER, GO.FFONT, 4, start=prevs[2], bounds=(-255, 255))
            G.Container.switches = [
                G.add_switch(GO.PRTOP, 40, prevs[0]),
                G.add_switch(GO.PRTOP, default=prevs[1])
            ]
            G.Container.colour = G.add_colour_pick(GO.PRTOP)
            G.uids[G.Container.colour].picker.p = prevs[4]
            TOPLEFT = GO.PSTATIC(10, 10) # Set a custom coordinate that never changes
            G.Container.scrollable, S = G.add_Scrollable(TOPLEFT, (250, 200), (250, 350))
            G.uids[G.Container.scrollable].scroll = prevTG[1]
            S.add_empty_space(GO.PCTOP, 10, 20)
            S.add_button('Scroll me!', GO.CBLUE, GO.PCTOP)
            G.Container.otherinp = S.add_input(GO.PCTOP, placeholder='I reset!!')
            S.add_button('Bye!', GO.CGREEN, GO.PCTOP)
            def pressed(elm):
                G.Container.txt = 'You pressed the button in the Scrollable :)'
                G.Reload()
            S.add_button('Press me!', GO.CRED, GO.PCTOP, callback=pressed)
            G.Container.otherswitch = S.add_switch(GO.PCTOP, default=prevTG[0])
        elif event == GO.ETICK: # This runs every 1/60 secs (each tick)
            return True # Return whether or not the loop should continue.
        elif event == GO.EELEMENTCLICK: # Some UI element got clicked!
            if element.type == GO.TBUTTON:
                # This gets passed 'element': the element that got clicked. TODO: make an Element class
                # The == means element's uid == __
                # UID gets generated based off order: so UID of 2 means second thing created that makes a UID.
                # When you create a thing that makes a UID it returns it. e.g. button1 = G.add_button(etc.)
                # So in that example button1 is the UID. Maybe try saving it to the container tho! Example shown by the exit button.
                if element == 2:
                    succeeded, ret = test_loading()
                    G.Container.txt = ('Ran for %i seconds%s' % (ret['i']+1, (' Successfully! :)' if succeeded else ' And failed :(')))
                    G.Reload()
                elif element == G.Container.exitbtn:
                    G.Abort()
                elif element == 1:
                    bot = GO.PNEW([0, 0], GO.PSTACKS[GO.PCBOTTOM][1], 1)
                    G.add_TextBox('HALLOOOO! :)', bot)
                    G.Container.idx = 0
                else:
                    G.Container.txt = element.txt # put name of button in middle
                    G.Reload()
            elif element.type == GO.TTEXTBOX:
                if G.Container.idx == 0:
                    element.set_text("Happy coding!")
                    G.Container.idx = 1
                else:
                    element.remove()
            elif element.type == GO.TINPUTBOX:
                G.Container.txt = element.txt
                element.remove()
                G.Reload()
        elif event == GO.EEVENT: # When something like a button is pressed. Is passed 'element' too, but this time it is an event
            if element.type == pygame.KEYDOWN:
                if element.key == pygame.K_s and element.mod & pygame.KMOD_CTRL:
                    G.Container.txt = 'Saved! (Don\'t worry - this does nothing)'
                    G.Reload()
            elif element.type == pygame.MOUSEBUTTONDOWN and element.button == pygame.BUTTON_RIGHT:
                opts = ['HI', 'BYE', 'HI AGAIN']
                resp = G.Dropdown(opts)
                if isinstance(resp, int):
                    G.Container.txt = opts[resp]
                    G.Reload()
        elif event == GO.ELAST:
            # This also gets passed 'aborted': Whether you aborted or exited the screen
            return {
                'Aborted?': aborted, 
                'Text in textbox': G.uids[G.Container.inp].get(),
                'Num in num textbox': G.uids[G.Container.numinp].get(),
                'Big switch state': G.uids[G.Container.switches[0]].get(),
                'Small switch state': G.uids[G.Container.switches[1]].get(),
                'Switch in scrollable area state': G.uids[G.Container.scrollable].G.uids[G.Container.otherswitch].get(),
                'Text in textbox in scrollable area': G.uids[G.Container.scrollable].G.uids[G.Container.otherinp].get()
                } # Whatever you return here will be returned by the function
    
    print(test('Right click! ' + t))
    pygame.quit() # this here for very fast quitting

def worldsDemo():
    from utils import World
    World('test', 'Test World', 'A world for testing random stuff', 25, quality=500, override=True)

def terrainGenDemo():
    from random import randint
    from utils import MapGen
    size = 1500
    n = 256
    inp = input('Input nothing to use random seed, input "." to use a preset good seed, or input your own INTEGER seed > ')
    if inp == '':
        map_seed = randint(0, 999999)
    elif inp == '.':
        map_seed = 762345
    else:
        map_seed = int(inp)
    useall = input('Type anything here to show all steps in terrain generation, or leave this blank and press enter to just show the finished product. > ') != ''
    outs, trees = MapGen(size, map_seed, n, useall=useall, showAtEnd=True).outs
    print(outs[0])
    pass

def LoadingDemo():
    import random, asyncio, pygame
    from graphics import Graphic
    from time import sleep
    G = Graphic()
    
    async def wait_random():
        seconds = random.randint(200, 2000) / 100
        #print(f"Waiting for {seconds} seconds...")
        await asyncio.sleep(seconds)
        #print(f"Done waiting for {seconds} seconds!")
        return seconds
    
    tasks = [wait_random() for _ in range(500)]
    print(G.PBLoading(tasks))
    
    @G.Loading
    def test_loading(self):
        for self.i in range(10):
            sleep(1)
    
    succeeded, ret = test_loading()
    pygame.quit()
    print('Ran for %i seconds%s' % (ret['i'], (' Successfully! :)' if succeeded else ' And failed :(')))

def ToastDemo():
    import pygame
    from graphics import Graphic
    from graphics import graphics_options as GO
    G = Graphic()
    @G.Graphic
    def func(event, *args, element=None, **kwargs):
        if event == GO.ELOADUI:
            G.Clear()
            G.add_text('Press the arrow keys!', GO.CBLACK, GO.PCCENTER)
        elif event == GO.ETICK:
            return True # Return whether or not the loop should continue.
        elif event == GO.EEVENT: # Passed 'element' (but is event)
            if element.type == pygame.KEYDOWN:
                if element.key == pygame.K_LEFT:
                    G.Toast('LEFT!', pos=GO.PLCENTER, col=GO.CBLUE)
                elif element.key == pygame.K_RIGHT:
                    G.Toast('RIGHT!', pos=GO.PRCENTER, col=GO.CYELLOW)
                elif element.key == pygame.K_UP:
                    G.Toast('UP!', pos=GO.PCTOP, col=GO.CGREEN)
                elif element.key == pygame.K_DOWN:
                    G.Toast('DOWN!', col=GO.CRED)
    func()
    pygame.quit()

def inputBoxDemo(): # TODO: update this
    import pygame as pg
    from graphics.GUI import InputBox
    screen = pg.display.set_mode((640, 480))
    input_box = InputBox(100, 100, 140, 32, 'type here!')
    print('output:', input_box.interrupt(screen))
    pg.quit()

def conversation_parserDemo():
    from utils.conversation_parse import Generator
    # If you run this file you can see these next statements at work
    # Each you can see is separated, by a like of ~~~~~~~~~~
    # You can see the different start params at work, with the same sample prompt
    def gen():
        g = Generator()
        yield g([(1, 2), 2])
        yield g([(0, 0), 3])
        yield g([(0, 3), 1])
        yield g([(3, 1), 2])
        yield g([(0, 2), 0])
        yield '\nAnd here are some randomly generated ones:\n' + g()
        while True:
            yield g()
    g = gen()
    print('Here are some I prepared earlier:\n')
    while True:
        print(next(g))
        if input() != '':
            break
def tinyLLMDemo():
    import asyncio
    from utils.bot import TinyLLM, lm
    tllm = TinyLLM()
    prompt = f"System: Reply as a helpful assistant. Currently {lm.get_date()}."
    while True:
        inp = input('> ')
        if inp == '': break
        prompt += f"\n\nUser: {inp}"
        i = asyncio.run(tllm.interrupt(inp))
        prompt += "\n\nAssistant:"
        end = asyncio.run(tllm(prompt))
        print(i)
        print(end)
        prompt += f" {end}"

def testLLMDemo():
    from utils.bot import test_tinyllm
    test_tinyllm()

def rateAIsDemo():
    import asyncio
    from utils.bot import rate_all
    asyncio.run(rate_all())

def api_keysDemo():
    from keys.api_keys import SaveAPIKeysDialog
    SaveAPIKeysDialog()

def node_editorDemo():
    from graphics import Graphic
    from elementGen import NodeSelector
    G = Graphic()
    print(NodeSelector(G, 2))

def node_parserDemo():
    from elementGen import allCategories, allNodes, Parse
    alls = allCategories()
    print('All categories and nodes:', {i: allNodes(i) for i in alls})
    tests = Parse('math')
    print('Test results of function Add with inputs 3 & 4:', tests('Add', 3, 4))

def switchDemo():
    import pygame
    from graphics.GUI import Switch
    pygame.init()
    win = pygame.display.set_mode()
    sprites = pygame.sprite.LayeredDirty()
    curpos = (10, 10)
    for _ in range(19):
        s = Switch(win, *curpos, size=10+2*_)
        sprites.add(s)
        sze = s.rect.size
        curpos = (curpos[0] + sze[0] + 10, curpos[1] + sze[1] + 10)
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    for i in sprites:
                        if i.rect.collidepoint(*pygame.mouse.get_pos()):
                            i.state = not i.state
        win.fill((255, 255, 255))
        sprites.update()
        pygame.display.update()
    pygame.quit()

def almostallgraphicsDemo():
    import pygame
    from pygame import locals
    from graphics.GUI import InputBox, TextBoxFrame
    from graphics.GUI.pyguix import gui as ui
    from graphics.GUI.textboxify.borders import LIGHT, BARBER_POLE

    class SnapHUDPartInfoExample(ui.SnapHUDPartInfo):

        # NOTE: Example bound function called by reflection OR by in game logic to update 'listening' SnapHUDPart:
        # This example simply allows for setting of value or getting current value when calling .part_one()
        # You can easily add other logic in part_one() that then updates the value when called. 
        # Yet still important is to return the part value.
        def part_one(self,v=None):
            return self.partinfo("part_one",v)

        def __init__(self) -> None:
            super().__init__()

    def textboxify_test(screen):
        # Customize and initialize a new dialog box.
        dialog_box = TextBoxFrame(
            text="Hello! This is a simple example of how TextBoxify can be implemented in Pygame games.",
            text_width=320,
            lines=2,
            pos=(80, 180),
            padding=(150, 100),
            font_color=(92, 53, 102),
            font_size=26,
            bg_color=(173, 127, 168),
            border=LIGHT,
        )

        # Optionally: add an animated or static image to indicate that the box is
        # waiting for user input before it continue to do anything else.
        # This uses the default indicator, but custom sprites can be used too.
        dialog_box.set_indicator()

        # Optionally: add a animated portrait or a static image to represent who is
        # talking. The portrait is adjusted to be the same height as the total line
        # height in the box.
        # This uses the default portrait, but custom sprites can be used too.
        dialog_box.set_portrait()

        # Create sprite group for the dialog boxes.
        dialog_group = pygame.sprite.LayeredDirty()
        #dialog_group.clear(screen, background)
        dialog_group.add(dialog_box)

        run = True
        next_quit = False
        while run:
            pygame.time.Clock().tick(60)
            screen.fill((92, 53, 102))
            all.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        shud.clicked()
                if event.type == locals.QUIT:
                    run = False
                if event.type == locals.KEYDOWN:
                    if event.key == locals.K_ESCAPE:
                        run = False

                    # Event that let the user tell the box to print next lines of
                    # text or close when finished printing the whole message.
                    if event.key == locals.K_RETURN:
                        if not dialog_box.alive():
                            dialog_group.add(dialog_box)
                        else:
                            # Cleans the text box to be able to go on printing text
                            # that didn't fit, as long as there are text to print out.
                            if dialog_box.words:
                                dialog_box.reset()

                            # Whole message has been printed and the box can now reset
                            # to default values, set a new text to print out and close
                            # down itself.
                            else:
                                dialog_box.reset(hard=True)
                                dialog_box.set_text("Happy coding!")
                                dialog_box.__border = BARBER_POLE
                                dialog_box.kill()
                                if next_quit:
                                    del dialog_box
                                    return
                                else:
                                    next_quit = True

            # Update the changes so the user sees the text.
            dialog_group.update()
            shud.update() # NOTE: update() called to check for 'hover'
            rects = dialog_group.draw(screen)
            pygame.display.update(rects)
            pygame.display.update()

    pygame.init()
    screen = pygame.display.set_mode((640, 360))

    all = pygame.sprite.RenderUpdates()

    shudpie = SnapHUDPartInfoExample()
    # NOTE: SnapHUD instance created AFTER the Info class instance.  
    shud = ui.SnapHUD(window=screen, rg=all, set_num_of_groups=0)

    run = True
    shudpie.part_one("None")
    while run:
        screen.fill((92, 53, 102))
        all.draw(screen)
        shud.update()
        pygame.display.update()
        mb = ui.MessageBox(
        window=screen,
        event_list=pygame.event.get(),
        buttons=['textboxify', 'input box'],
        )

        # NOTE: Act upoon if the MessageBox was canceled, if not can act upon the .clicked() value.:
        if not mb.canceled():
            if mb.clicked() == 'textboxify':
                textboxify_test(screen)
            else:
                input_box = InputBox(100, 100, 140, 32, 'Type here!')
                def _(screen):
                    all.draw(screen)
                    shud.update()
                def __(event):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == pygame.BUTTON_LEFT:
                            shud.clicked()
                out = input_box.interrupt(screen, run_too=_, event_callback=__)
                shudpie.part_one(out)
        else:
            print("You canceled the MessageBox instance.")
            run = False

def overlaysDemo():
    from overlay import Overlay, tk
    from time import sleep
    o = Overlay((200, 200), (10, 10))

    def hideAndSeek():
        o.hide()
        sleep(1)
        o.show()

    tk.Button(o(), text='destroy!', command=o.destroy).pack()
    tk.Button(o(), text='Hide for 1 second!!', command=hideAndSeek).pack()
    while o.running(): pass

def scrollableDemo():
    import pygame
    from graphics.GUI import Scrollable
    pygame.init()
    w = pygame.display.set_mode()
    from tkinter.filedialog import askopenfilename
    im = pygame.image.load(askopenfilename(defaultextension='.png', filetypes=[('.png', '.png'), ('.jpg', '.jpg')]))
    S = Scrollable(im, (20, 20), (500, 500), (0, im.get_height()-500))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEWHEEL:
                S.update(event)
        w.fill((0, 0, 0))
        S(w)
        pygame.display.update()

def LDtkAPPDemo():
    from ldtk import LDtkAPP
    app = LDtkAPP()
    app.launch()
    app.wait_for_win()
    winopen = True
    while winopen:
        winopen = app.is_win_open()

if __name__ == '__main__':
    import tkinter as Tk # Because everyone has tkinter
    from tkinter.scrolledtext import ScrolledText
    root = Tk.Tk()
    def cmd(cmdd):
        root.destroy()
        print('loading...')
        cmdd()
    def rcmd(cmdd):
        root.protocol("WM_DELETE_WINDOW", load)
        for widget in root.winfo_children():
            widget.destroy()
        E = ScrolledText(root,  
                         wrap = Tk.WORD,  
                         width = 40,  
                         height = 10,
                         state=Tk.DISABLED)
        E.pack(fill=Tk.BOTH, side=Tk.LEFT, expand=True)
        def npr(*txts, sep='  '):
            E.config(state=Tk.NORMAL)
            E.insert(Tk.END,sep.join([str(i) for i in txts])+'\n')
            E.config(state=Tk.DISABLED)
            root.update()
        def ninp(prompt=''):
            class blank: pass
            b = blank()
            b.done = False
            def run():
                v = E2.get()
                for widget in root.winfo_children():
                    if widget != E and not E in widget.winfo_children(): widget.destroy()
                b.done = True
                b.res = v
            Tk.Label(root, text=prompt).pack()
            E2 = Tk.Entry(root)
            E2.pack()
            E2.bind("<Return>", lambda *args: run())
            Tk.Button(root, command=lambda *args: run(), text='GO!').pack()
            root.update()
            while b.done == False: root.update()
            return b.res
        oprint = print
        globals()['print'] = npr
        oinput = input
        globals()['input'] = ninp
        oprint('Loading please wait...')
        print('Loading please wait...')
        root.update()
        try:
            cmdd()
        except Exception as e:
            print('AN EXCEPTION HAS OCURRED:', type(e), e, sep='\n') # Breakpoint here and in console use
            # `e.with_traceback()`
        globals()['print'] = oprint
        globals()['input'] = oinput
        
    def load():
        for widget in root.winfo_children():
            widget.destroy()
        Tk.Button(root, text='EXIT', command=root.destroy).pack()
        
        Tk.Label (root, text='Node stuff:').pack()
        Tk.Button(root, text='Node Editor Demo',        command=lambda: cmd(node_editorDemo)                    ).pack()
        Tk.Button(root, text='Node Parser Demo',        command=lambda: rcmd(node_parserDemo), relief=Tk.RIDGE  ).pack()

        Tk.Label (root, text='Graphics stuff:').pack()
        Tk.Button(root, text='Graphics Demo',           command=lambda: cmd(GraphicsDemo)                       ).pack()
        Tk.Button(root, text='Loading Demo',            command=lambda: cmd(LoadingDemo)                        ).pack()
        Tk.Button(root, text='Toast Demo',              command=lambda: cmd(ToastDemo)                          ).pack()
        Tk.Button(root, text='Switch Demo',             command=lambda: cmd(switchDemo)                         ).pack()
        Tk.Button(root, text='Input Box Demo',          command=lambda: cmd(inputBoxDemo)                       ).pack()
        Tk.Button(root, text='Scrollable Demo',         command=lambda: cmd(scrollableDemo)                     ).pack()
        Tk.Button(root, text='Other Graphics Demo',     command=lambda: cmd(almostallgraphicsDemo)              ).pack()

        Tk.Label (root, text='Generation stuff:').pack()
        Tk.Button(root, text='Generate World Demo',     command=lambda: rcmd(worldsDemo), relief=Tk.RIDGE       ).pack()
        Tk.Button(root, text='Generate Terrain Demo',   command=lambda: rcmd(terrainGenDemo), relief=Tk.RIDGE   ).pack()

        Tk.Label (root, text='AI stuff:').pack()
        Tk.Button(root, text='TinyLLM Demo',            command=lambda: rcmd(tinyLLMDemo), relief=Tk.RIDGE      ).pack()
        Tk.Button(root, text='Test LLM Demo',           command=lambda: rcmd(testLLMDemo), relief=Tk.RIDGE      ).pack()
        Tk.Button(root, text='Rate AIs Demo',           command=lambda: rcmd(rateAIsDemo), relief=Tk.RIDGE      ).pack()
        
        Tk.Label (root, text='Other stuff:').pack()
        Tk.Button(root, text='API Keys Demo',           command=lambda: cmd(api_keysDemo),                      ).pack()
        Tk.Button(root, text='Overlays Demo',           command=lambda: cmd(overlaysDemo),                      ).pack()
        Tk.Button(root, text='LDtk app Demo',           command=lambda: cmd(LDtkAPPDemo),                       ).pack()
        Tk.Button(root, text='Conversation Parse Demo', command=lambda: cmd(conversation_parserDemo), relief=Tk.SUNKEN ).pack()
        root.protocol("WM_DELETE_WINDOW", root.destroy)
    load()
    def btt():
        root.attributes('-topmost', True)
    root.after(1, btt)
    root.mainloop()
