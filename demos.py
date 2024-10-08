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
            G.Container.inp = G.add_input(GO.PCCENTER, GO.FFONT, maximum=16, start=prevs[3])
            G.add_empty_space(GO.PCCENTER, 0, 50)
            G.Container.numinp = G.add_num_input(GO.PCCENTER, GO.FFONT, 4, start=prevs[2], bounds=(-255, 255))
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
            G.Container.otherinp = S.add_input(GO.PCTOP, placeholder='I reset!!')
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

def OCollisionsDemo(debug=False):
    import os
    if debug:
        os.environ['debug'] = 'True'
    from demoFiles import collisionsDemo

if __name__ == '__main__':
    opts = {}
    def add_opt(name, cmd):
        idx = len(opts)
        print(f"{idx}: {name}")
        opts[str(idx)] = cmd
    print('Type one of the numbers to run that command. Type anything but them to quit.\nPlease keep in mind most of these probably won\'t work or will re removed in the future.')
        
    print('Node stuff:') # Nodes
    add_opt('Node Editor Demo',        NNodeEditorDemo                 )
    add_opt('Node Parser Demo',        NNodeParserDemo                 )

    print('Graphics stuff:') # BlazeSudio.graphics
    add_opt('Graphics Demo',           GGraphicsDemo                   )
    add_opt('Loading Demo',            GLoadingDemo                    )
    add_opt('Toast Demo',              GToastDemo                      )
    add_opt('Switch Demo',             GSwitchDemo                     )
    add_opt('Colour Picker Demo',      GColourPickDemo                 )
    add_opt('Input Box Demo',          GInputBoxDemo                   )
    add_opt('Scrollable Demo',         GScrollableDemo                 )
    add_opt('Dropdown Demo',           GDropdownDemo                   )
    add_opt('Other Graphics Demo',     GOtherGraphicsDemo              )

    print('Generation stuff:') # Terrain
    add_opt('Generate World Demo',     TWorldsDemo                     )
    add_opt('Generate Terrain Demo',   TTerrainGenDemo                 )

    print('AI stuff:') # Ai
    add_opt('TinyLLM Demo',            ATinyLLMDemo                    )
    add_opt('Test LLM Demo',           ATestLLMDemo                    )
    add_opt('Rate AIs Demo',           ARateAIsDemo                    )
    
    print('Other stuff:') # Other
    add_opt('Overlays Demo',           OOverlaysDemo,                  )
    add_opt('LDtk app Demo',           OLDtkAPPDemo,                   )
    add_opt('Collisions Demo',         OCollisionsDemo,                )
    add_opt('DEBUG Collisions Demo',   lambda: OCollisionsDemo(True)   )
    add_opt('Conversation Parse Demo', OConversationParserDemo         )
    i = input("> ")
    if i in opts:
        print('Loading demo...')
        opts[i]()
    else:
        print('Could not find demo! Quitting...')
