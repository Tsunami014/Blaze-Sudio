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

def MCollisionsDemo(debug=False):
    import os
    if debug:
        os.environ['debug'] = 'True'
    from demoFiles import collisionsDemo

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
