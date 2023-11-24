import pygame, os, pickle
import graphics.graphics_options as GO
import elementGen.node_parser as np

categories = [i.name for i in os.scandir('data/elements') if i.is_dir()]

nodes = [np.Parse(i) for i in np.allCategories()]

def mouseDown(button=1):
    i = False
    while True:
        r = pygame.mouse.get_pressed(3)[button-1]
        yield ((i != r and r), r)
        i = r

def NodeSelector(G, continue_to_edit=0):
    """Makes a Node Selector screen!

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
                self.iteminfo = [pickle.load(open('data/elements/%s/%s'%(category, i.name), 'rb')) for i in self.items]
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

# Make delete category/node file
# As well as a NodeEditor screen have a NodeRenderer screen, which is also used in NodeEditor

def CAT(txt, front=True, bgcol=GO.CWHITE, colour=GO.CGREEN, colour2=None, filled=False): # Circle And Text
    t = GO.FFONT.render(txt, 2, GO.CBLACK)
    sze = GO.FFONT.size('a')[1]
    poschange = t.get_height() - sze
    sur = pygame.Surface((t.get_width() + sze + 5, t.get_height()+poschange))
    sur.fill(bgcol)
    cir = None
    if front:
        cir = pygame.Rect(0, 0, sze, sze)
        pygame.draw.circle(sur, GO.CAWHITE, (sze//2, t.get_height()//2), sze//2-2)
        pygame.draw.circle(sur, colour, (sze//2, t.get_height()//2), sze//2-2, 5)
        if colour2 != None:
            csur = pygame.Surface((sze, sze//2))
            csur.fill(GO.CAWHITE)
            pygame.draw.circle(csur, colour2, (sze//2, 0), sze//2-2, 5)
            sur.blit(csur, (0, t.get_height()//2))
        if filled: pygame.draw.circle(sur, GO.CGREY, (sze//2, t.get_height()//2), sze//4)
        pygame.draw.circle(sur, GO.CBLACK, (sze//2, t.get_height()//2), sze//2, 2)
        sur.blit(t, (sze + 5, poschange))
    else:
        cir = pygame.Rect(t.get_width() + 5, 0, sze, sze)
        pygame.draw.circle(sur, GO.CAWHITE, (t.get_width() + 5 + sze//2, t.get_height()//2), sze//2-2)
        pygame.draw.circle(sur, colour, (t.get_width() + 5 + sze//2, t.get_height()//2), sze//2-2, 5)
        if colour2 != None:
            csur = pygame.Surface((sze, sze//2))
            csur.fill(GO.CAWHITE)
            pygame.draw.circle(csur, colour2, (sze//2, 0), sze//2-2, 5)
            sur.blit(csur, (t.get_width() + 5, t.get_height()//2))
        if filled: pygame.draw.circle(sur, GO.CGREY, (t.get_width() + 5 + sze//2, t.get_height()//2), sze//4)
        pygame.draw.circle(sur, GO.CBLACK, (t.get_width() + 5 + sze//2, t.get_height()//2), sze//2, 2)
        sur.blit(t, (0, poschange))
    return sur, cir

def NodeEditor(G, path):
    """Makes a Node Editor screen!

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
            G.Container.saved = False
            G.Container.md = [
                mouseDown(), # Left mouse button
                mouseDown(3) # Right mouse button
            ]
            G.Container.selecting = None
            if path.endswith('.elm'):
                path = path[:-4]
            if not os.path.exists('data/elements/'+path+'.elm'):
                pickle.dump({"idea": "BLANK", "name": "New File", "version": 2}, open('data/elements/'+path+'.elm', 'wb+'))
            G.Container.contents = pickle.load(open('data/elements/'+path+'.elm', 'rb'))
            if 'nodes' in G.Container.contents:
                G.Container.nodes = G.Container.contents['nodes']
            else:
                G.Container.nodes = []
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
                    RTOP = GO.PNEW([0, 1], GO.PSTACKS[GO.PRTOP][1], 1)
                    LTOP = GO.PNEW([0, 1], GO.PSTACKS[GO.PLTOP][1], 2)
                    G.Clear()
                    G.add_text('SETTINGS FOR NODE "%s":'%G.Container.name, GO.CGREEN, LTOP, GO.FFONT)
                    G.Container.inpname = G.add_input(LTOP, width=G.size[0]/3, resize=GO.RNONE, placeholder=G.Container.name)
                    G.add_text('SETTINGS FOR NODE EDITOR:', GO.CBLUE, RTOP, GO.FFONT)
                    G.add_empty_space(CBOT, -20, 0)
                    G.Container.go = G.add_button('Apply!', GO.CGREEN, CBOT)
                    G.Container.exit = G.add_button('Cancel', GO.CGREY, CBOT)
                elif event == GO.ETICK: return True
                elif event == GO.EELEMENTCLICK:
                    if element == G.Container.go:
                        G.Container.went = True
                        G.Abort()
                    elif element == G.Container.exit:
                        G.Container.went = False
                        G.Abort()
                elif event == GO.ELAST:
                    if G.Container.went: # Not cancelled
                        res = G.uids[G.Container.inpname].text
                        if res != '':
                            G.Container.name = res
                            G.Container.contents['name'] = res
                        pass # Whatever you return here will be returned by the function
            settings()
        elif event == GO.ETICK:
            cirs = []
            for p, node in G.Container.nodes:
                col = GO.CBLUE
                txt = GO.FFONT.render(str(node), 2, GO.CBLACK)
                sur = pygame.Surface(G.size)
                sur.fill(col)
                sur.blit(txt, (0, 0))
                start = txt.get_height() + 5
                i = start
                mx = txt.get_width()
                for name, typ in node.inputs:
                    s, c = CAT(name, bgcol=col)
                    c.move_ip(0+p[0], i+p[1])
                    cirs.append((c, node))
                    sur.blit(s, (0, i))
                    mx = max(mx, s.get_width())
                    i += s.get_height() + 2
                if node.outputs != []:
                    mx += 20
                i2 = start
                mx2 = 0
                for name, typ in node.outputs:
                    s, c = CAT(name, front=False, bgcol=col)
                    c.move_ip(mx+p[0], i2+p[1])
                    cirs.append((c, node))
                    sur.blit(s, (mx, i2))
                    mx2 = max(mx2, s.get_width())
                    i2 += s.get_height() + 2
                mx2 += mx
                sur2 = pygame.Surface((mx2, max(i, i2)))
                sur2.fill(col)
                sur2.blit(sur, (0, 0))
                pygame.draw.rect(G.WIN, col, pygame.Rect(*p, mx2+10, max(i, i2)+10), border_radius=8)
                G.WIN.blit(sur2, (p[0]+5, p[1]+5))
            lf, l = next(G.Container.md[0])
            # lf = left mouse button first press, l = left mouse button is being pressed
            rf, r = next(G.Container.md[1])
            # Same with r
            
            if not l: G.Container.selecting = None
            for i in cirs:
                if i[0].collidepoint(pygame.mouse.get_pos()):
                    G.WIN.blit(CAT('', filled=True, bgcol=col)[0], (i[0].topleft[0]+5, i[0].topleft[1]+7))
                    if lf:
                        G.Container.selecting = (i[1], (i[0].center[0]+5, i[0].center[1]+7))
            
            if G.Container.selecting != None:
                pygame.draw.line(G.WIN, GO.CRED, G.Container.selecting[1], pygame.mouse.get_pos(), 10)
            return True
        elif event == GO.EEVENT: # When something like a button is pressed. Is passed 'element' too, but this time it is an event
            if element.type == pygame.KEYDOWN:
                if element.key == pygame.K_s and element.mod & pygame.KMOD_CTRL:
                    if path.endswith('.elm'):
                        path = path[:-4]
                    G.Container.contents['nodes'] = G.Container.nodes
                    pickle.dump(G.Container.contents, open('data/elements/'+path+'.elm', 'wb+')) # Save
                    G.Container.saved = True
            elif element.type == pygame.MOUSEBUTTONDOWN and element.button == pygame.BUTTON_RIGHT:
                p = pygame.mouse.get_pos()
                kgo = True
                while kgo:
                    resp = G.Dropdown([str(i) for i in nodes], pos=p)
                    if isinstance(resp, int):
                        resp2 = G.Dropdown(['Back']+[str(i) for i in nodes[resp].getall()], pos=p)
                        if isinstance(resp2, int):
                            if resp2 != 0:
                                G.Container.nodes.append((p, nodes[resp].getall()[resp2-1]))
                                kgo = False
                        else: kgo = False
                    else: kgo = False
        elif event == GO.ELAST:
            if G.Container.saved:
                if path.endswith('.elm'):
                    path = path[:-4]
                if G.Container.name != path.split('/')[1]:
                    os.remove('data/elements/'+path+'.elm')
                    path = path.split('/')[0] + '/' + G.Container.name
                    open('data/elements/'+path+'.elm', 'wb+')
                    pickle.dump(G.Container.contents, open('data/elements/'+path+'.elm', 'wb+'))
    return editor(path)
