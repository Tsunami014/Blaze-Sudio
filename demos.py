import tkinter as Tk # Because everyone has tkinter

def loadingDemo():
    import pygame
    from graphics import Loading
    from time import sleep
    @Loading
    def f(self):
        for self.i in range(10):
            sleep(1)
    pygame.init()
    WIN = pygame.display.set_mode()
    font = pygame.font.Font(None, 64)
    succeeded, ret = f(WIN, font)
    pygame.quit()
    print('Ran for %i seconds%s' % (ret['i'], (' Successfully! :)' if succeeded else ' And failed :(')))
    print('end')

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
        elif event == GO.EEVENT: # When something like a button is pressed. Is passed 'element' too, but this time it is an event
            if element.type == pygame.KEYDOWN:
                if element.key == pygame.K_SPACE:
                    G.Container.txt = 'You pressed space!'
                    G.Reload()
        elif event == GO.ELAST:
            # This also gets passed 'aborted': Whether you aborted or exited the screen
            return aborted # Whatever you return here will be returned by the function
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

def async_handlingDemo():
    import random, asyncio, pygame
    from graphics import Graphic
    G = Graphic()
    
    async def wait_random():
        seconds = random.randint(200, 2000) / 100
        #print(f"Waiting for {seconds} seconds...")
        await asyncio.sleep(seconds)
        #print(f"Done waiting for {seconds} seconds!")
        return seconds
    
    tasks = [wait_random() for _ in range(500)]
    G.PBLoading(tasks)
    pygame.quit()

if __name__ == '__main__':
    root = Tk.Tk()
    def cmd(cmdd):
        root.quit()
        cmdd()
    Tk.Button(root, text='Loading Demo', command=lambda: cmd(loadingDemo)).pack()
    Tk.Button(root, text='Graphics Demo', command=lambda: cmd(GraphicsDemo)).pack()
    Tk.Button(root, text='Generate World Demo', command=lambda: cmd(worldsDemo)).pack()
    Tk.Button(root, text='Generate Terrain Demo', command=lambda: cmd(terrainGenDemo)).pack()
    Tk.Button(root, text='Async Progressbar Demo', command=lambda: cmd(async_handlingDemo)).pack()
    root.mainloop()
