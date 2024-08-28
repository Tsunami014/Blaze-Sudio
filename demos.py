from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Hide the annoying pygame thing
from threading import Thread

# TODO: update everything that needs to be updated

# I think that the things need to be by themselves
# What I mean by that is, let's take BlazeSudio.graphics as an example;
# With things like the dropdown and the input boxes, they are
# Implemented in the main BlazeSudio.graphics class, but the demos should test
# Their individual code, not how they work in a class

CATEGORYNAMES = {
    'N': 'Nodes',
    'G': 'BlazeSudio.graphics',
    'T': 'Terrain',
    'A': 'AI',
    'O': 'Other'
}

# NODE STUFF

def NNodeEditorDemo():
    from BlazeSudio.elementGen import NodeSelector
    print(NodeSelector(2))

def NNodeParserDemo():
    from BlazeSudio.elementGen import allCategories, allNodes, Parse
    alls = allCategories()
    print('All categories and nodes:', {i: allNodes(i) for i in alls})
    tests = Parse('math')
    print('Test results of function Add with inputs 3 & 4:', tests('Add', 3, 4))

# BlazeSudio.graphics STUFF

def GGraphicsDemo():
    import pygame
    import BlazeSudio.graphics.options as GO
    from BlazeSudio.graphics import Graphic
    from time import sleep
    G = Graphic()
    @G.Loading
    def test_loading(self):
        for self.i in range(10):
            sleep(1)
    
    @G.Graphic
    def test(event, txt, element=None, aborted=False): # You do not need args and kwargs if you KNOW that your function will not take them in. Include what you need.
        if event == GO.ELOADUI: # Load the graphics in!
            CTOP = GO.PNEW((1, 0), GO.PCTOP.func) # Bcos usually the Center Top makes the elements stack down, so I make a new thing that stacks sideways
            LBOT = GO.PNEW((0, -1), GO.PLBOTTOM.func)
            # Attempt to load previous values
            try:
                prevs = [i.get() for i in (G.Container.switches+[G.Container.numinp,G.Container.inp])] + [G.Container.colour.picker.p]
                prevTG = [G.Container.otherswitch.get(), G.Container.scrollable.scroll]
            except:
                prevs = [False, False, 0, '', (0, 0.5)]
                prevTG = [False, 0]
            G.Clear()
            G.add_text('HI', GO.CGREEN, GO.PRBOTTOM, GO.FTITLE)
            G.add_text(':) ', GO.CBLACK, GO.PRBOTTOM, GO.FTITLE)
            G.add_empty_space(GO.PCCENTER, 0, -150) # Yes, you can have negative space. This makes the next things shifted the other direction.
            G.add_text('This is a cool thing', GO.CBLUE, GO.PCCENTER)
            G.add_text('Sorry, I meant a cool TEST', GO.CRED, GO.PCCENTER)
            G.Container.txt = G.add_text(txt, GO.CGREEN, GO.PCCENTER)
            G.add_empty_space(LBOT, 0, 20)
            G.add_button('Button 1 :D', GO.CYELLOW, LBOT)
            G.add_text('Buttons above [^] and below [v]', GO.CBLUE, LBOT)
            G.Container.TextboxBtn = G.add_button('Textbox test', GO.CBLUE, LBOT)
            G.Container.LoadingBtn = G.add_button('Loading test', GO.CGREEN, LBOT)
            G.Container.exitbtn = G.add_button('EXIT', GO.CRED, GO.PLCENTER)
            G.add_empty_space(CTOP, -150, 0) # Center it a little more
            G.add_text('Are you ', GO.CBLACK, CTOP)
            G.add_text('happy? ', GO.CGREEN, CTOP)
            G.add_text('Or sad?', GO.CRED, CTOP)
            G.Container.inp = G.add_input(GO.PCCENTER, GO.FFONT, maximum=16)
            G.add_empty_space(GO.PCCENTER, 0, 50)
            G.Container.numinp = G.add_num_input(GO.PCCENTER, GO.FFONT, 4, bounds=(-255, 255))
            G.Container.switches = [
                G.add_switch(GO.PRTOP, 40, speed=1, default=prevs[0]),
                G.add_switch(GO.PRTOP, default=prevs[1])
            ]
            G.Container.colour = G.add_colour_pick(GO.PRTOP)
            G.Container.colour.picker.p = prevs[4]
            TOPLEFT = GO.PSTATIC(10, 10) # Set a custom coordinate that never changes
            S, G.Container.scrollable = G.add_Scrollable(TOPLEFT, (250, 200), (250, 350))
            G.Container.scrollable.scroll = prevTG[1]
            S.add_empty_space(GO.PCTOP, 10, 20)
            S.add_button('Scroll me!', GO.CBLUE, GO.PCTOP)
            S.add_button('Hello!', GO.CYELLOW, GO.PCTOP)
            S.add_button('Bye!', GO.CGREEN, GO.PCTOP)
            def pressed(elm):
                G.Container.txt.set('You pressed the button in the Scrollable :)')
            S.add_button('Press me!', GO.CRED, GO.PCTOP, callback=pressed)
            G.Container.otherswitch = S.add_switch(GO.PCTOP, default=prevTG[0])
        elif event == GO.ETICK: # This runs every 1/60 secs (each tick)
            pass # Return False if you want to quit the screen. This is not needed if you never want to do this.
        elif event == GO.EELEMENTCLICK: # Some UI element got clicked!
            if element.type == GO.TBUTTON:
                # This gets passed 'element': the element that got clicked. TODO: make an Element class
                # The == means element's uid == __
                # UID gets generated based off order: so UID of 2 means second thing created that makes a UID.
                # When you create a thing that makes a UID it returns it. e.g. button1 = G.add_button(etc.)
                # So in that example button1 is the UID. Maybe try saving it to the container tho! Example shown by the exit button.
                if element == G.Container.LoadingBtn:
                    succeeded, ret = test_loading()
                    G.Container.txt.set('Ran for %i seconds%s' % (ret.i+1, (' Successfully! :)' if succeeded else ' And failed :(')))
                elif element == G.Container.exitbtn:
                    G.Abort()
                elif element == G.Container.TextboxBtn:
                    bot = GO.PNEW((0, 0), GO.PCBOTTOM.func, 1)
                    G.add_TextBox('HALLOOOO! :)', bot)
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
                    G.Toast('Saved! (Don\'t worry - this does nothing)')
            elif element.type == pygame.MOUSEBUTTONDOWN and element.button == pygame.BUTTON_RIGHT:
                opts = ['HI', 'BYE', 'HI AGAIN']
                resp = G.Dropdown(opts)
                if isinstance(resp, int):
                    G.Container.txt.set(opts[resp])
        elif event == GO.ELAST:
            # This also gets passed 'aborted': Whether you aborted or exited the screen
            return {
                'Aborted?': aborted, 
                'Text in textbox': G.Container.inp.get(),
                'Num in num textbox': G.Container.numinp.get(),
                'Big switch state': G.Container.switches[0].get(),
                'Small switch state': G.Container.switches[1].get(),
                'Switch in scrollable area state': G.Container.otherswitch.get(),
                'Text in textbox in scrollable area': G.Container.otherinp.get()
                } # Whatever you return here will be returned by the function
    
    print(test('Right click or press anything or press ctrl+s!'))
    pygame.quit() # this here for very fast quitting

def GDropdownDemo():
    import pygame
    from BlazeSudio.utils import dropdown
    pygame.init()
    win = pygame.display.set_mode()
    run = True
    while run:
        win.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
                dropdown(win, ['HI', 'BYE', 'HI AGAIN'])
        pygame.display.update()
    pygame.quit()

def GLoadingDemo():
    import random, asyncio, pygame
    from BlazeSudio.graphics import Graphic
    from time import sleep
    G = Graphic()
    
    async def wait_random():
        seconds = random.randint(200, 2000) / 100
        #print(f"Waiting for {seconds} seconds...")
        await asyncio.sleep(seconds)
        #print(f"Done waiting for {seconds} seconds!")
        return seconds
    
    tasks = [wait_random() for _ in range(500)]
    print(G.PBLoading(tasks)[1]() or 'You quit the loading! Why?')
    
    @G.Loading
    def test_loading(self):
        for self.i in range(10):
            sleep(1)
    
    succeeded, ret = test_loading()
    pygame.quit()
    print('Ran for %i seconds%s' % (ret.i, (' Successfully! :)' if succeeded else ' And failed :(')))

def GToastDemo():
    import pygame
    from BlazeSudio.graphics import Graphic
    from BlazeSudio.graphics import options as GO
    G = Graphic()
    @G.Graphic
    def func(event, *args, element=None, **kwargs):
        if event == GO.ELOADUI:
            G.Clear()
            G.add_text('Press the arrow keys!', GO.CBLACK, GO.PCCENTER)
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

def GInputBoxDemo():
    import pygame as pg
    from BlazeSudio.graphics.GUI import InputBox
    screen = pg.display.set_mode((640, 480))
    input_box = InputBox(100, 100, 140, 32, 'type here!')
    print('output:', input_box.interrupt(screen))
    pg.quit()

def GColourPickDemo():
    import pygame
    from BlazeSudio.graphics.GUI import ColourPickerBTN
    from BlazeSudio.graphics import Thing, CustomGraphic, handle_events
    pygame.init()
    window = pygame.display.set_mode((500, 500))
    G = CustomGraphic(window) 
    clock = pygame.time.Clock()

    cp = Thing(ColourPickerBTN(window, 50, 50))

    run = True
    while run:
        clock.tick(100)
        evs, run = handle_events()
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[2]:
            mp = pygame.mouse.get_pos()
            cp.pos = (mp[0]-cp.size//2, mp[1]-cp.size//2)

        window.fill(0)
        cp.update_obj(evs, G)
        pygame.display.flip()
        
    pygame.quit()

def GSwitchDemo():
    import pygame
    from BlazeSudio.graphics.GUI import Switch
    from BlazeSudio.graphics import Stuff, CustomGraphic, handle_events
    pygame.init()
    win = pygame.display.set_mode()
    stuff = Stuff()
    stuff.add('switches')
    curpos = (10, 10)
    for _ in range(19):
        s = Switch(win, *curpos, size=10+2*_)
        stuff['switches'].append(s)
        sze = s.rect.size
        curpos = (curpos[0] + sze[0] + 10, curpos[1] + sze[1] + 10)
    
    G = CustomGraphic(win)
    run = True
    while run:
        evs, run = handle_events()
        win.fill((255, 255, 255))
        stuff.update_all(evs, G)
        pygame.display.update()
    pygame.quit()

def GOtherGraphicsDemo(): # TODO: Evaluate whether the stuff in this is worth keeping
    import pygame
    from pygame import locals
    from BlazeSudio.graphics.GUI import InputBox, TextBoxFrame
    from BlazeSudio.graphics.GUI.pyguix import gui as ui
    from BlazeSudio.graphics.GUI.textboxify.borders import LIGHT, BARBER_POLE

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

def OOverlaysDemo():
    from BlazeSudio.overlay import Overlay, tk
    from time import sleep
    o = Overlay((200, 200), (10, 10))

    def hideAndSeek():
        o.hide()
        sleep(1)
        o.show()

    tk.Button(o(), text='destroy!', command=o.destroy).pack()
    tk.Button(o(), text='Hide for 1 second!!', command=hideAndSeek).pack()
    o2 = Overlay((200, 50), (200, 200), on_destroy=lambda: print('HA nice try but you ain\'t destroying THIS window'))
    tk.Label(o2(), text='I WILL NEVER BE DESTROYED').pack()
    while o.running(): pass

def GScrollableDemo():
    import pygame
    from BlazeSudio.graphics.GUI import Scrollable
    pygame.init()
    w = pygame.display.set_mode()
    from tkinter.filedialog import askopenfilename
    im = pygame.image.load(askopenfilename(defaultextension='.png', filetypes=[('.png', '.png'), ('.jpg', '.jpg')]))
    S = Scrollable(im, (20, 20), (500, 500), (0, im.get_height()-500))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
                break
            elif event.type == pygame.MOUSEWHEEL:
                S.event_handle(event)
        w.fill((0, 0, 0))
        S(w)
        pygame.display.update()

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
    for txt in m.generate(size, map_seed, n, useall=useall, showAtEnd=True): print(txt)
    outs, trees = m.outs
    print(outs[0])
    pass

# AI STUFF

def ATinyLLMDemo():
    import asyncio
    from BlazeSudio.bot import TinyLLM, lm
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

def ATestLLMDemo():
    from BlazeSudio.bot import test_tinyllm
    test_tinyllm()

def ARateAIsDemo():
    import asyncio
    from BlazeSudio.bot import rate_all
    asyncio.run(rate_all())

# OTHER STUFF

def ODemoTest():
    from time import sleep
    r = True
    while r:
        print('This is a demo test!')
        sleep(2)
        print('This tests to make sure that the demo software is working.')
        sleep(4)
        if input('Understand? (y/n) >').lower() == 'y':
            r = False
    print('Good. See you soon!')
    sleep(3)

def OConversationParserDemo():
    from BlazeSudio.conversation_parse import Generator
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

def OLDtkAPPDemo():
    from BlazeSudio.ldtk import LDtkAPP
    app = LDtkAPP()
    app.launch()
    app.wait_for_win()
    winopen = True
    while winopen:
        winopen = app.is_win_open()
        try:
            app.make_full()
        except:
            winopen = False

def OCollisionsDemo():
    from BlazeSudio.utils import collisions
    from BlazeSudio.graphics.options import CRAINBOWCOLOURS, FFONT
    import pygame
    pygame.init()
    win = pygame.display.set_mode()
    run = True
    header_opts = ['point', 'line', 'circle', 'rect', 'rotated rect', 'polygon', 'eraser', 'help']
    typ = 0
    curObj = collisions.Point(0, 0)
    objs = collisions.Shapes()
    dir = [0, 0, 0]
    pos = [0, 0]
    accel = [0, 0]
    
    def drawObj(obj, t, col):
        if t == 5:
            if isinstance(obj, collisions.Point):
                pygame.draw.circle(win, col, (obj.x, obj.y), 8)
            elif isinstance(obj, collisions.Line):
                pygame.draw.line(win, col, obj.p1, obj.p2, 8)
            else:
                for line in obj.toLines():
                    pygame.draw.line(win, col, line.p1, line.p2, 8)
        if t == 0 or t == 6:
            pygame.draw.circle(win, ((255, 255, 255) if t == 6 else col), (obj.x, obj.y), 8)
        elif t == 1:
            pygame.draw.line(win, col, obj.p1, obj.p2, 8)
        elif t == 2:
            pygame.draw.circle(win, col, (obj.x, obj.y), obj.r, 8)
        elif t == 3:
            pygame.draw.rect(win, col, (obj.x, obj.y, obj.w, obj.h), 8) # TODO: Rects with negative width and hei
        elif t == 4:
            for line in obj.toLines():
                pygame.draw.line(win, col, line.p1, line.p2, 8)
    
    def moveCurObj(curObj):
        if typ == 1:
            curObj.p1 = pos
            curObj.p2 = (curObj.p1[0]+dir[0], curObj.p1[1]+dir[1])
        elif typ == 5:
            if isinstance(curObj, collisions.Point):
                curObj.x, curObj.y = pos
            elif isinstance(curObj, collisions.Line):
                curObj.p2 = pos
            else:
                curObj.points[-1] = pos
        else:
            curObj.x, curObj.y = pos
            if typ == 2:
                curObj.r = dir[1]
            elif typ == 3:
                curObj.w, curObj.h = dir[0], dir[1]
            elif typ == 4:
                curObj.w, curObj.h = dir[0], dir[1]
                curObj.rot = dir[2]
        return curObj
    
    clock = pygame.time.Clock()
    while run:
        playMode = pygame.key.get_mods() & pygame.KMOD_ALT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
                elif event.key == pygame.K_SPACE:
                    if typ == 6:
                        for i in objs.copy_leave_shapes():
                            if i.collides(curObj):
                                objs.remove_shape(i)
                    else:
                        objs.add_shape(curObj)
                        if typ == 5:
                            curObj = curObj = collisions.Point(*pygame.mouse.get_pos())
                        else:
                            curObj = curObj.copy()
                elif event.key == pygame.K_COMMA and typ == 5:
                    if isinstance(curObj, collisions.Point):
                        curObj = collisions.Line(curObj.getTuple(), pygame.mouse.get_pos())
                    elif isinstance(curObj, collisions.Line):
                        curObj = collisions.Polygon(curObj.p1, curObj.p2, pygame.mouse.get_pos())
                    else:
                        curObj.points += [pygame.mouse.get_pos()]
                elif event.key == pygame.K_r:
                    objs = collisions.Shapes()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the header_opts that got clicked, if any
                if event.pos[1] < 50:
                    oldtyp = typ
                    typ = event.pos[0]//(win.get_width()//len(header_opts))
                    if typ == 0:
                        curObj = collisions.Point(*event.pos)
                    elif typ == 1:
                        curObj = collisions.Line((0, 0), (10, 10))
                        dir = [50, 100, 0]
                    elif typ == 2:
                        curObj = collisions.Circle(*event.pos, 100)
                        dir = [0, 100, 0]
                    elif typ == 3:
                        curObj = collisions.Rect(*event.pos, 100, 100)
                        dir = [100, 100, 0]
                    elif typ == 4:
                        curObj = collisions.RotatedRect(*event.pos, 100, 100, 45)
                        dir = [100, 100, 45]
                    elif typ == 5:
                        curObj = collisions.Point(*event.pos)
                    elif typ == 6:
                        curObj = collisions.Point(*event.pos)
                    else: # Last item in list - help menu
                        pygame.draw.rect(win, (155, 155, 155), (win.get_width()//4, win.get_height()//4, win.get_width()//2, win.get_height()//2), border_radius=8)
                        win.blit(FFONT.render("""How to use:
Click on one of the options at the top to change your tool. Pressing space adds it to the board. The up, down, left and right arrow keys as well as comma and full stop do stuff with some of them too.
Holding shift in this mode shows some normals!
And holding alt allows you to test the movement physics. Holding shift and alt makes the movement physics have gravity!
And pressing 'r' will reset everything to nothing without warning.
 
 
Press any key/mouse to close this window""",0,allowed_width=win.get_width()//2-4), (win.get_width()//4+2, win.get_height()//4+2))
                        run2 = True
                        pygame.display.update()
                        while run2:
                            for ev in pygame.event.get():
                                if ev.type == pygame.QUIT or ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame.KEYDOWN:
                                    run2 = False
                            clock.tick(60)
                        typ = oldtyp
        
        btns = pygame.key.get_pressed()
        if btns[pygame.K_UP]:
            dir[1] -= 5
        if btns[pygame.K_DOWN]:
            dir[1] += 5
        if btns[pygame.K_LEFT]:
            dir[0] -= 5
        if btns[pygame.K_RIGHT]:
            dir[0] += 5
        if btns[pygame.K_COMMA]:
            dir[2] -= 5
        if btns[pygame.K_PERIOD]:
            dir[2] += 5
        
        if btns[pygame.K_w]:
            accel[1] -= 1
        if btns[pygame.K_s]:
            accel[1] += 1
        if btns[pygame.K_a]:
            accel[0] -= 1
        if btns[pygame.K_d]:
            accel[0] += 1
            
        win.fill((0, 0, 0) if (not objs.collides(curObj)) or playMode else (250, 50, 50))
        pygame.draw.rect(win, (255, 255, 255), (0, 0, win.get_width(), 50))
        # Split it up into equal segments and put the text header_opts[i] in the middle of each segment
        for i in range(len(header_opts)):
            pygame.draw.line(win, (0, 0, 0), (i*win.get_width()//len(header_opts), 0), (i*win.get_width()//len(header_opts), 50))
            font = pygame.font.Font(None, 36)
            text = font.render(header_opts[i], True, (0, 0, 0))
            win.blit(text, (i*win.get_width()//len(header_opts)+10, 10))
        
        if playMode:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                accel[1] += 0.2
            accellLimits = [10, 10]
            accel = [min(max(accel[0], -accellLimits[0]), accellLimits[0]), min(max(accel[1], -accellLimits[1]), accellLimits[1])]
            gravity = [0.02, 0.02]
            def grav_eff(x, grav):
                if x < -grav:
                    return x + grav
                if x > grav:
                    return x - grav
                return 0
            accel = [grav_eff(accel[0], gravity[0]), grav_eff(accel[1], gravity[1])]
            _, accel = curObj.handleCollisionsAccel(accel, objs)

        else:
            pos = pygame.mouse.get_pos()
            accel = [0, 0]
            curObj = moveCurObj(curObj)
        
        for i in objs:
            drawObj(i, [collisions.Point, collisions.Line, collisions.Circle, collisions.Rect, collisions.RotatedRect, collisions.Polygon].index(type(i)), (10, 255, 50))
        drawObj(curObj, typ, CRAINBOWCOLOURS[typ])

        if not playMode:
            for i in objs.whereCollides(curObj):
                pygame.draw.circle(win, (175, 155, 155), i, 8)
            
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                mpos = pygame.mouse.get_pos()
                for o in objs:
                    cs = o.whereCollides(curObj)
                    for i in cs:
                        pygame.draw.line(win, (0, 0, 0), i, collisions.rotate(i, [i[0], i[1]-50], o.tangent(i, [i[0]-mpos[0], i[1]-mpos[1]])-90), 8) # tangent -90 = normal
        
        pygame.display.update()
        clock.tick(60)

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
        def go():
            cmdd()
            globals()['print'] = oprint
            globals()['input'] = oinput
            return
            # Spare code
            try:
                cmdd()
            except Exception as e:
                print('AN EXCEPTION HAS OCURRED:', type(e), e, sep='\n') # Breakpoint here and in console use
                # `e.with_traceback()`
        t = Thread(target=go, daemon=False)
        t.start()
        
    def load():
        for widget in root.winfo_children():
            widget.destroy()
        Tk.Button(root, text='EXIT', command=root.destroy).pack()
        
        Tk.Label (root, text='Node stuff:').pack() # Nodes
        Tk.Button(root, text='Node Editor Demo',        command=lambda: cmd(NNodeEditorDemo)                    ).pack()
        Tk.Button(root, text='Node Parser Demo',        command=lambda: rcmd(NNodeParserDemo), relief=Tk.RIDGE  ).pack()

        Tk.Label (root, text='Graphics stuff:').pack() # BlazeSudio.graphics
        Tk.Button(root, text='Graphics Demo',           command=lambda: cmd(GGraphicsDemo)                       ).pack()
        Tk.Button(root, text='Loading Demo',            command=lambda: cmd(GLoadingDemo)                        ).pack()
        Tk.Button(root, text='Toast Demo',              command=lambda: cmd(GToastDemo)                          ).pack()
        Tk.Button(root, text='Switch Demo',             command=lambda: cmd(GSwitchDemo)                         ).pack()
        Tk.Button(root, text='Colour Picker Demo',      command=lambda: cmd(GColourPickDemo)                     ).pack()
        Tk.Button(root, text='Input Box Demo',          command=lambda: cmd(GInputBoxDemo)                       ).pack()
        Tk.Button(root, text='Scrollable Demo',         command=lambda: cmd(GScrollableDemo)                     ).pack()
        Tk.Button(root, text='Dropdown Demo',           command=lambda: cmd(GDropdownDemo)                       ).pack()
        Tk.Button(root, text='Other Graphics Demo',     command=lambda: cmd(GOtherGraphicsDemo)                  ).pack()

        Tk.Label (root, text='Generation stuff:').pack() # Terrain
        Tk.Button(root, text='Generate World Demo',     command=lambda: rcmd(TWorldsDemo), relief=Tk.RIDGE       ).pack()
        Tk.Button(root, text='Generate Terrain Demo',   command=lambda: rcmd(TTerrainGenDemo), relief=Tk.RIDGE   ).pack()

        Tk.Label (root, text='AI stuff:').pack() # Ai
        Tk.Button(root, text='TinyLLM Demo',            command=lambda: rcmd(ATinyLLMDemo), relief=Tk.RIDGE      ).pack()
        Tk.Button(root, text='Test LLM Demo',           command=lambda: rcmd(ATestLLMDemo), relief=Tk.RIDGE      ).pack()
        Tk.Button(root, text='Rate AIs Demo',           command=lambda: rcmd(ARateAIsDemo), relief=Tk.RIDGE      ).pack()
        
        Tk.Label (root, text='Other stuff:').pack() # Other
        Tk.Button(root, text='Overlays Demo',           command=lambda: cmd(OOverlaysDemo),                      ).pack()
        Tk.Button(root, text='LDtk app Demo',           command=lambda: cmd(OLDtkAPPDemo),                       ).pack()
        Tk.Button(root, text='Collisions Demo',         command=lambda: cmd(OCollisionsDemo),                    ).pack()
        Tk.Button(root, text='Conversation Parse Demo', command=lambda: cmd(OConversationParserDemo), relief=Tk.SUNKEN ).pack()
        root.protocol("WM_DELETE_WINDOW", root.destroy)
    load()
    def btt():
        root.attributes('-topmost', True)
    root.after(1, btt)
    root.mainloop()
