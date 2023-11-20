import graphics.graphics_options as GO
import pygame, os, json
from time import sleep

categories = [
    'characters',
    'tilemaps',
    'others'
]

def NodeSelector(G, continue_to_edit=0):
    """Makes a Node Selector screen! Still in progress. Come back later!

    Parameters
    ----------
    G : graphics.Graphic
        The Graphic screen
    continue_to_edit : int, optional
        Whether to, once selected, return (0 & default), run the editor and exit once the editor gets exited (1) OR go back into select dialog when exit (2)
    
    USE:
```py
from graphics import Graphic
G = Graphic()
NodeSelector(G)
```
    """
    @G.Graphic
    def item_select(event, category, element=None, aborted=False):
        if event == GO.EFIRST:
            @G.Loading
            def load(self):
                self.items = [i for i in os.scandir('data/elements/'+category) if i.is_file()]
                self.iteminfo = [json.load(open('data/elements/%s/%s'%(category, i.name))) for i in self.items]
                self.subs = ['Go back to the previous page', 'Make a new item from scratch'] + [i['idea'] for i in self.iteminfo]
            cont, res = load()
            G.Container.res = res
            G.Container.txt = ''
            G.Container.prevpresses = []
            if not cont: G.Abort()
        elif event == GO.ELOADUI:
            G.Clear()
            G.add_text(category + ' item selection', GO.CBLACK, GO.PCTOP)
            G.add_text(G.Container.txt, GO.CBLUE, GO.PCTOP)
            G.add_button('Back', GO.CGREY, GO.PLTOP)
            G.add_button('New Item', GO.CGREEN, GO.PLTOP)
            cols = GO.CRAINBOW()
            for i in G.Container.res['iteminfo']:
                G.add_button(i['name'], next(cols), GO.PLCENTER)
        elif event == GO.ETICK:
            if G.touchingbtns != G.Container.prevpresses:
                G.Container.prevpresses = G.touchingbtns.copy()
                try: G.Container.txt = G.Container.res['subs'][G.get_idx(G.touchingbtns[0])]
                except: G.Container.txt = ''
                G.Reload()
            return True
        elif event == GO.EELEMENTCLICK: # Passed 'element'
            if element == 0: # back
                return False
            elif element == 1: # make new world
                return 'NEW'
            else:
                return G.Container.res['items'][element.uid-2].name
    @G.Graphic
    def category_select(event, element=None, aborted=False):
        if event == GO.ELOADUI:
            G.Clear()
            G.add_text('Category selection', GO.CBLACK, GO.PCTOP)
            G.add_button('Back', GO.CGREY, GO.PLTOP)
            G.add_button('New Category', GO.CGREEN, GO.PLTOP)
            cols = GO.CRAINBOW()
            for i in categories:
                G.add_button(i, next(cols), GO.PLCENTER)
        elif event == GO.ETICK:
            return True
        elif event == GO.EELEMENTCLICK: # Passed 'element'
            if element == 0: # back
                return None
            elif element == 1: # make new world
                if continue_to_edit == 1 or continue_to_edit == 2:
                    NodeEditor(G, 'NEW/NEW')
                if continue_to_edit != 2:
                    return 'NEW/NEW'
            else:
                name = element.txt
                selection = item_select(name)
                if selection != False and selection != None:
                    pth = name + '/' + selection
                    if continue_to_edit == 1 or continue_to_edit == 2:
                        NodeEditor(G, pth)
                    if continue_to_edit != 2:
                        return pth
    return category_select()

# Select element to edit screen (copy world select)
# Each category of elements is a sub-folder under data/elements/
# As well as a NodeEditor screen have a NodeRenderer screen, which is also used in NodeEditor

def NodeEditor(G, path):
    """Makes a Node Editor screen! Still in progress. Come back later!

    Parameters
    ----------
    G : graphics.Graphic
        The Graphic screen
    path : str
        The path to the currently editing Node. e.g. 'Other/niceness'
    
    USE:
```py
from graphics import Graphic
G = Graphic()
NodeEditor(G)
```
    """
    @G.Graphic
    def editor(event, path, element=None, aborted=False):
        if event == GO.EFIRST:
            if path.endswith('.elm'):
                path = path[:-4]
            if not os.path.exists('data/elements/'+path+'.elm'):
                open('data/elements/'+path+'.elm', 'w+').write('{"idea": "BLANK", "name": "New File"}')
            G.Container.contents = json.load(open('data/elements/'+path+'.elm'))
            G.Container.name = G.Container.contents['name']
        if event == GO.ELOADUI:
            G.Clear()
            G.add_text('EDITING ELEMENT "%s"'%G.Container.name, GO.CGREEN, GO.PCTOP, GO.FTITLE)
            G.add_button('Settings', GO.CGREEN, GO.PRTOP)
        elif event == GO.EELEMENTCLICK: # This is going to be the only button that was created
            @G.Graphic
            def settings(event, element=None, aborted=False):
                if event == GO.ELOADUI:
                    CBOT = GO.PNEW([1, 0], GO.PSTACKS[GO.PCBOTTOM][1], 0)
                    G.Clear()
                    G.add_empty_space(CBOT, -20, 0)
                    G.Container.go = G.add_button('Apply!', GO.CGREEN, CBOT)
                    G.Container.exit = G.add_button('Cancel', GO.CGREY, CBOT)
                elif event == GO.ETICK: return True
                elif event == GO.EELEMENTCLICK:
                    if element == G.Container.go:
                        print('GO!')
                        G.Abort()
                    elif element == G.Container.exit:
                        print('Cancel. :(')
                        G.Abort()
                elif event == GO.ELAST:
                    pass # Whatever you return here will be returned by the function
            settings()
        elif event == GO.ETICK:
            return True
        elif event == GO.EEVENT: # When something like a button is pressed. Is passed 'element' too, but this time it is an event
            if element.type == pygame.KEYDOWN:
                if element.key == pygame.K_s and event.mod & pygame.KMOD_SHIFT:
                    json.dump(G.Container.contents, open('data/elements/'+path+'.elm', 'w+')) # Save
    return editor(path)
