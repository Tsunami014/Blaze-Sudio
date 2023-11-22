import tkinter as Tk # Because everyone has tkinter

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
            CTOP = GO.PNEW([1, 0], GO.PSTACKS[GO.PCTOP][1], 0) # Bcos usually the Center Top makes the elements stack down, so I make a new thing that stacks sideways
            G.Clear()
            G.add_text('HI', GO.CGREEN, GO.PRBOTTOM, GO.FTITLE)
            G.add_text(':) ', GO.CBLACK, GO.PRBOTTOM, GO.FTITLE)
            G.add_empty_space(GO.PCCENTER, 0, -150) # Yes, you can have negative space. This makes the next things shifted the other direction.
            G.add_text('This is a cool thing', GO.CBLUE, GO.PCCENTER)
            G.add_text('Sorry, I meant a cool TEST', GO.CRED, GO.PCCENTER)
            G.add_text(G.Container.txt, GO.CGREEN, GO.PCCENTER)
            G.add_empty_space(GO.PCBOTTOM, 0, 20)
            G.add_button('Button 1 :D', GO.CYELLOW, GO.PCBOTTOM)
            G.add_text('Buttons above [^] and below [v]', GO.CBLUE, GO.PCBOTTOM)
            G.add_button('Textbox test', GO.CBLUE, GO.PCBOTTOM)
            G.add_button('Loading test', GO.CGREEN, GO.PCBOTTOM)
            G.Container.exitbtn = G.add_button('EXIT', GO.CRED, GO.PCBOTTOM)
            G.add_empty_space(CTOP, -150, 0) # Center it a little more
            G.add_text('Are you ', GO.CBLACK, CTOP)
            G.add_text('happy? ', GO.CGREEN, CTOP)
            G.add_text('Or sad?', GO.CRED, CTOP)
            G.Container.inp = G.add_input(GO.PCCENTER, GO.FFONT, maximum=16)
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
        elif event == GO.ELAST:
            # This also gets passed 'aborted': Whether you aborted or exited the screen
            return (aborted, G.uids[G.Container.inp].text) # Whatever you return here will be returned by the function
    print(test(t))
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

def inputBoxDemo(): # TODO: make part of Graphic class
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
    from api_keys import SaveAPIKeysDialog
    SaveAPIKeysDialog()

def node_editorDemo():
    from graphics import Graphic
    from elementGen import NodeEditor
    G = Graphic()
    NodeEditor(G)

def node_parserDemo():
    from elementGen import allCategories, allNodes, Parse
    alls = allCategories()
    print('All categories and nodes:', {i: allNodes(i) for i in alls})
    tests = Parse('test')
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


if __name__ == '__main__':
    root = Tk.Tk()
    def cmd(cmdd):
        root.destroy()
        cmdd()
    Tk.Button(root, text='Node Editor Demo',        command=lambda: cmd(node_editorDemo)        ).pack()
    Tk.Button(root, text='Node Parser Demo',        command=lambda: cmd(node_parserDemo)        ).pack()
    Tk.Button(root, text='Loading Demo',            command=lambda: cmd(LoadingDemo)            ).pack()
    Tk.Button(root, text='Graphics Demo',           command=lambda: cmd(GraphicsDemo)           ).pack()
    Tk.Button(root, text='Other Graphics Demo',     command=lambda: cmd(almostallgraphicsDemo)  ).pack()
    Tk.Button(root, text='Generate World Demo',     command=lambda: cmd(worldsDemo)             ).pack()
    Tk.Button(root, text='Generate Terrain Demo',   command=lambda: cmd(terrainGenDemo)         ).pack()
    Tk.Button(root, text='Input Box Demo',          command=lambda: cmd(inputBoxDemo)           ).pack()
    Tk.Button(root, text='TinyLLM Demo',            command=lambda: cmd(tinyLLMDemo)            ).pack()
    Tk.Button(root, text='Test LLM Demo',           command=lambda: cmd(testLLMDemo)            ).pack()
    Tk.Button(root, text='Rate AIs Demo',           command=lambda: cmd(rateAIsDemo)            ).pack()
    Tk.Button(root, text='API Keys Demo',           command=lambda: cmd(api_keysDemo)           ).pack()
    Tk.Button(root, text='Switch Demo',             command=lambda: cmd(switchDemo)             ).pack()
    Tk.Button(root, text='Conversation Parse Demo', command=lambda: cmd(conversation_parserDemo)).pack()
    root.mainloop()
