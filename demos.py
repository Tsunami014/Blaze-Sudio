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
    from elementGen import NodeSelector
    G = Graphic()
    print(NodeSelector(G, 2))

if __name__ == '__main__':
    root = Tk.Tk()
    def cmd(cmdd):
        root.destroy()
        cmdd()
    Tk.Button(root, text='Loading Demo', command=lambda: cmd(LoadingDemo)).pack()
    Tk.Button(root, text='Graphics Demo', command=lambda: cmd(GraphicsDemo)).pack()
    Tk.Button(root, text='Generate World Demo', command=lambda: cmd(worldsDemo)).pack()
    Tk.Button(root, text='Generate Terrain Demo', command=lambda: cmd(terrainGenDemo)).pack()
    Tk.Button(root, text='Input Box Demo', command=lambda: cmd(inputBoxDemo)).pack()
    Tk.Button(root, text='Conversation Parse Demo', command=lambda: cmd(conversation_parserDemo)).pack()
    Tk.Button(root, text='TinyLLM Demo', command=lambda: cmd(tinyLLMDemo)).pack()
    Tk.Button(root, text='Test LLM Demo', command=lambda: cmd(testLLMDemo)).pack()
    Tk.Button(root, text='Rate AIs Demo', command=lambda: cmd(rateAIsDemo)).pack()
    Tk.Button(root, text='API Keys Demo', command=lambda: cmd(api_keysDemo)).pack()
    Tk.Button(root, text='Node Editor Demo', command=lambda: cmd(node_editorDemo)).pack()
    root.mainloop()
