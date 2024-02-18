import pygame, os, dill
import graphics.graphics_options as GO
import elementGen.node_parser as np
import elementGen.types as Ts

categories = [i.name for i in os.scandir('data/elements') if i.is_dir()]

alls = []
nodes = []
for i in np.allCategories():
    j = np.Parse(i, alls)
    nodes.append(j)

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
                self.iteminfo = [dill.load(open('data/elements/%s/%s'%(category, i.name), 'rb')) for i in self.items]
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
            for i in G.Container.res.iteminfo:
                G.add_button(i['name'], next(cols), GO.PLCENTER)
        elif event == GO.ETICK:
            if G.touchingbtns != G.Container.prevpresses:
                G.Container.prevpresses = G.touchingbtns.copy()
                try: G.Container.txt = G.Container.res.subs[G.get_idx(G.touchingbtns[0])]
                except: G.Container.txt = ''
                G.Reload()
            return True
        elif event == GO.EELEMENTCLICK: # Passed 'element'
            if element == 0: # back
                return False
            elif element == 1: # make new world
                return 'NEW'
            else:
                return G.Container.res.items[element.uid-2].name
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

def CAT(txt, front=True, bgcol=GO.CWHITE, colour=GO.CGREEN, colour2=None, filled=False, docircle=True): # Circle And Text
    t = GO.FFONT.render(txt, 2, GO.CBLACK)
    sze = GO.FFONT.size('a')[1]
    poschange = t.get_height() - sze
    sur = pygame.Surface((t.get_width() + sze + 5, t.get_height()+poschange))
    sur.fill(bgcol)
    cir = None
    if not docircle:
        sur.blit(t, (0, poschange))
        cir = pygame.Rect(0, 0, 0, 0)
    elif front:
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
    def dropdown():
        p = pygame.mouse.get_pos()
        while True:
            resp = G.Dropdown([str(i) for i in nodes], pos=p)
            if isinstance(resp, int) and not isinstance(resp, bool):
                resp2 = G.Dropdown(['Back']+[str(i) for i in nodes[resp].getall()], pos=p)
                if isinstance(resp2, int) and not isinstance(resp, bool):
                    if resp2 != 0:
                        G.Container.nodes.append((p, nodes[resp].getall()[resp2-1].copy()))
                        return True
                else: return False
            else: return False
    
    def parse(i, l, lf, rd):
        if not l and isinstance(G.Container.selecting, tuple) and i.isntsimilar(G.Container.selecting[0]):
            if not G.Container.DONTDOIT: G.Container.highlighting = None
            if i.rect.collidepoint(pygame.mouse.get_pos()):
                d = False
                for j in range(len(G.Container.connections)):
                    k = [_ for _ in G.Container.connections[j] if _.isinp][0]
                    if i == k or G.Container.selecting[0] == k:
                        G.Container.connections[j][0].connectedto = None
                        G.Container.connections[j][1].connectedto = None
                        G.Container.connections[j] = [G.Container.selecting[0], i]
                        G.Container.selecting[0].connectedto = i.gen_CT(G.Container.nodes)
                        i.connectedto = G.Container.selecting[0].gen_CT(G.Container.nodes)
                        d = True
                        break
                if not d:
                    G.Container.connections.append([G.Container.selecting[0], i])
                    G.Container.selecting[0].connectedto = i.gen_CT(G.Container.nodes)
                    i.connectedto = G.Container.selecting[0].gen_CT(G.Container.nodes)
        elif not l and isinstance(G.Container.selecting, list) and G.Container.selecting[2] == pygame.mouse.get_pos():
            # did not move, so select
            G.Container.highlighting = G.Container.selecting[3]
        elif G.Container.selecting == None or (isinstance(G.Container.selecting, tuple) and i.isntsimilar(G.Container.selecting[0])):
            if i.rect.collidepoint(pygame.mouse.get_pos()):
                rd.append((i.rect.topleft[0]+5, i.rect.topleft[1]+7))
                if lf:
                    G.Container.selecting = (i, (i.rect.center[0]+5, i.rect.center[1]+7))
                    if not G.Container.DONTDOIT: G.Container.highlighting = None
        return rd
    
    @G.Graphic
    def editor(event, path, element=None, aborted=False):
        if event == GO.EFIRST:
            G.Container.saved = False
            G.Container.md = [
                mouseDown(), # Left mouse button
                mouseDown(3) # Right mouse button
            ]
            G.Container.selecting = None
            G.Container.highlighting = None
            G.Container.DONTDOIT = False
            if path.endswith('.elm'):
                path = path[:-4]
            if not os.path.exists('data/elements/'+path+'.elm'):
                # Version: major.minor
                dill.dump({"idea": "BLANK", "name": "New File", "version": "0.4"}, open('data/elements/'+path+'.elm', 'wb+'))
            # TODO: version checking and updating (not for versions less than 1.0 which is the liftoff version)
            G.Container.contents = dill.load(open('data/elements/'+path+'.elm', 'rb'))
            if 'nodes' in G.Container.contents:
                G.Container.nodes = G.Container.contents['nodes']
            else:
                G.Container.nodes = []
            if 'connections' in G.Container.contents:
                G.Container.connections = G.Container.contents['connections']
            else:
                G.Container.connections = []
            G.Container.name = G.Container.contents['name']
        if event == GO.ELOADUI:
            G.Clear()
            G.add_text('%s'%G.Container.name, GO.CGREEN, GO.PCTOP, GO.FTITLE)
            G.add_button('Settings', GO.CGREEN, GO.PRTOP)
        elif event == GO.EELEMENTCLICK: # This is going to be the only button that was created
            @G.Graphic
            def settings(event, element=None, aborted=False):
                if event == GO.ELOADUI:
                    CBOT = GO.PNEW([1, 0], GO.PSTACKS[GO.PCBOTTOM][1])
                    RTOP = GO.PNEW([0, 1], GO.PSTACKS[GO.PRTOP][1])
                    LTOP = GO.PNEW([0, 1], GO.PSTACKS[GO.PLTOP][1])
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
            lf, l = next(G.Container.md[0])
            # lf = left mouse button first press, l = left mouse button is being pressed
            rf, r = next(G.Container.md[1])
            # Same with r
            
            w, h = G.size[0] / 8 * 3, G.size[1] / 8 * 3
            rec = pygame.Rect(8, G.size[1]-h-8, w, h)
            G.Container.DONTDOIT = rec.collidepoint(*pygame.mouse.get_pos())
            
            rd = []
            for p, node in G.Container.nodes:
                g = node.get(G.Container.nodes)
                node.cirs.reset()
                col = GO.CBLUE
                txt = GO.FFONT.render(str(node), 2, GO.CBLACK)
                sur = pygame.Surface(G.size)
                sur.fill(col)
                sur.blit(txt, (0, 0))
                start = txt.get_height() + 5
                i = start
                mx = txt.get_width()
                for n in node.inputs:
                    name = n.name
                    if 'Remove' in node.data and n.name in node.data['Remove']: continue
                    if n.connectedto is not None:
                        gotten = n.get_CT(G.Container.nodes).get_P(G.Container.nodes).get(G.Container.nodes)
                    if n.connectedto is not None and \
                        n.get_CT(G.Container.nodes).name in gotten and \
                            gotten[n.get_CT(G.Container.nodes).name] != Ts.defaults[Ts.strtypes[n.get_CT(G.Container.nodes).type]]:
                                name += '='+str(gotten[n.get_CT(G.Container.nodes).name])
                    elif n.value != Ts.defaults[Ts.strtypes[n.type]] or n.type == bool: name += ':'+str(n.value)
                    rmn = True
                    try: rmn = n.name not in node.data['KeepName']
                    except: pass
                    if rmn and name != n.name: name = name[len(n.name)+1:]
                    dc = True
                    try: dc = n.name not in node.data['RMInp']
                    except: pass
                    s, c = CAT(name, bgcol=col, docircle=dc)
                    c.move_ip(0+p[0], i+p[1])
                    node.cirs[n] = c
                    sur.blit(s, (0, i))
                    mx = max(mx, s.get_width())
                    i += s.get_height() + 2
                    rd = parse(n, l, lf, rd)
                if node.outputs != []:
                    mx += 20
                i2 = start
                mx2 = 0
                for n in node.outputs:
                    if 'Remove' in node.data and n.name in node.data['Remove']: continue
                    name = n.name
                    rmn = True
                    try: rmn = n.name not in node.data['KeepName']
                    except: pass
                    if n.name in g:
                        if rmn: name = str(g[n.name])
                        else: name += ':'+str(g[n.name])
                    dc = True
                    try: dc = n.name not in node.data['RMInp']
                    except: pass
                    s, c = CAT(name, front=False, bgcol=col, docircle=dc)
                    c.move_ip(mx+p[0], i2+p[1])
                    node.cirs[n] = c
                    sur.blit(s, (mx, i2))
                    mx2 = max(mx2, s.get_width())
                    i2 += s.get_height() + 2
                    rd = parse(n, l, lf, rd)
                mx2 += mx
                sur2 = pygame.Surface((mx2, max(i, i2)))
                sur2.fill(col)
                sur2.blit(sur, (0, 0))
                r = pygame.Rect(*p, mx2+10, max(i, i2)+10)
                pygame.draw.rect(G.WIN, col, r, border_radius=8)
                if G.Container.highlighting == node:
                    pygame.draw.rect(G.WIN, GO.CACTIVE, pygame.Rect(p[0]-15, p[1]-15, mx2+40, max(i, i2)+40), width=10, border_radius=8)
                if G.Container.selecting == None and lf and r.collidepoint(pygame.mouse.get_pos()):
                    if not G.Container.DONTDOIT:  G.Container.highlighting = None
                    G.Container.selecting = [G.Container.nodes.index((p, node)), (pygame.mouse.get_pos()[0]-p[0], pygame.mouse.get_pos()[1]-p[1]), pygame.mouse.get_pos(), node]
                G.WIN.blit(sur2, (p[0]+5, p[1]+5))
            for i in rd:
                G.WIN.blit(CAT('', filled=True, bgcol=col)[0], i)
            
            if not l and G.Container.selecting != None:
                G.Container.selecting = None
            
            if isinstance(G.Container.selecting, tuple):
                pygame.draw.line(G.WIN, GO.CRED, G.Container.selecting[1], pygame.mouse.get_pos(), 10)
            elif isinstance(G.Container.selecting, list):
                G.Container.nodes[G.Container.selecting[0]] = (
                    (pygame.mouse.get_pos()[0]-G.Container.selecting[1][0],
                     pygame.mouse.get_pos()[1]-G.Container.selecting[1][1]), 
                    G.Container.nodes[G.Container.selecting[0]][1])
            
            for i in G.Container.connections:
                pygame.draw.line(G.WIN, GO.CNEW('orange'), \
                    (i[0].rect.center[0]+5, i[0].rect.center[1]+7), \
                    (i[1].rect.center[0]+5, i[1].rect.center[1]+7), 10)
            
            if G.Container.highlighting != None:
                w, h = G.size[0] / 8 * 3, G.size[1] / 8 * 3
                pygame.draw.rect(G.WIN, GO.CNEW('light grey'), rec, border_radius=8)
                node = G.Container.highlighting
                txt = GO.FFONT.render(str(node), 2, GO.CBLACK)
                G.WIN.blit(txt, ((w - txt.get_width())/2+8, G.size[1]-h+10))
                if G.scrollsables == []:
                    pos = GO.PSTATIC(12, G.size[1]-h+10+txt.get_height()+2)
                    adds = [[], []]
                    boxes = []
                    getsize = lambda: sum([max(adds[0][i][2].get_height(),boxes[i][2][1])+10 for i in range(len(adds[0]))])
                    for i in node.inputs:
                        r = GO.FFONT.render(i.name+':', 2, GO.CBLACK)
                        s = getsize()
                        adds[0].append((5, s, r))
                        boxes.append((r.get_width()+7, s, Ts.sizing[Ts.strtypes[i.type]](i.value, GO.FFONT), Ts.strtypes[i.type], i.value))
                    g = node.get(G.Container.nodes)
                    for i in node.outputs:
                        name = i.name
                        if n.name in g: name += ':'+str(g[n.name])
                        r = GO.FFONT.render(name, 2, GO.CBLACK)
                        adds[1].append((w-r.get_width()-10, sum([i[2].get_height()+10 for i in adds[1]]), r))
                    size = max(getsize(), sum([i[2].get_height()+10 for i in adds[1]]))
                    size = max(size, h-(txt.get_height()+30)+1)
                    _, scr = G.add_Scrollable(pos, (w-8, h-(txt.get_height()+30)), (w-8, size), 2, True)
                    scr.bgcol = GO.CNEW('light grey')
                    scr.Container.outs = []
                    scr.Container.adds = [adds[0], []]
                    for i in adds[0]:
                        scr.add_surface(i[2], GO.PSTATIC(i[0], i[1]))
                    for i in adds[1]:
                        scr.add_surface(i[2], GO.PSTATIC(i[0], i[1]))
                        scr.Container.outs.append(scr.statics[-1])
                    for i in boxes:
                        if i[3] == 'int':
                            scr.add_num_input(GO.PSTATIC(i[0], i[1]), font=GO.FFONT, width=10, start=i[4])
                        elif i[3] == 'str':
                            scr.add_input(GO.PSTATIC(i[0], i[1]), font=GO.FFONT, width=GO.FFONT.size('c'*10)[0], start=i[4])
                        elif i[3] == 'bool':
                            scr.add_switch(GO.PSTATIC(i[0], i[1]), default=i[4])
                        elif i[3] == 'any':
                            scr.add_input(GO.PSTATIC(i[0], i[1]), font=GO.FFONT, width=GO.FFONT.size('c'*10)[0], start=str(i[4]))
                else:
                    scr = G.scrollsables[0].G
                    adds = scr.Container.adds
                    getsize = lambda: sum([max(adds[0][i][2].get_height(),boxes[i][2][1])+10 for i in range(len(adds[0]))])
                    inps = scr.uids
                    for i in range(len(node.inputs)):
                        node.inputs[i].value = inps[i].get()
                    for i in scr.Container.outs: scr.statics.remove(i)
                    scr.Container.outs = []
                    g = node.get(G.Container.nodes)
                    for i in node.outputs:
                        name = i.name
                        if n.name in g: name += ':'+str(g[n.name])
                        r = GO.FFONT.render(name, 2, GO.CBLACK)
                        scr.add_surface(r, GO.PSTATIC(w-r.get_width()-10, sum([i[2].get_height()+10 for i in adds[1]])))
                        scr.Container.outs.append(scr.statics[-1])
                    outs = G.scrollsables[0].G.statics
            elif G.scrollsables != []:
                G.Reload()
            return True
        elif event == GO.EEVENT: # When something like a button is pressed. Is passed 'element' too, but this time it is an event
            if element.type == pygame.MOUSEBUTTONDOWN:
                if not G.Container.DONTDOIT: G.Container.highlighting = None
            
            if element.type == pygame.KEYDOWN:
                if element.key == pygame.K_s and element.mod & pygame.KMOD_CTRL:
                    G.Toast('Saving...')
                    if path.endswith('.elm'):
                        path = path[:-4]
                    G.Container.contents['nodes'] = G.Container.nodes
                    G.Container.contents['connections'] = G.Container.connections
                    dill.dump(G.Container.contents, open('data/elements/'+path+'.elm', 'wb+')) # Save
                    G.Container.saved = True
                    G.toasts = []
                    G.Toast('Saved!')
                elif element.key == pygame.K_DELETE:
                    if G.Container.highlighting != None:
                        n = G.Container.nodes[
                                [i[1] for i in G.Container.nodes].index(G.Container.highlighting)
                            ][1]
                        cs = n.inputs + n.outputs
                        for i in cs:
                            ct = i.get_CT(G.Container.nodes)
                            if ct != None: ct.connectedto = None
                        delL = []
                        for i in G.Container.connections:
                            if i[0] in cs or i[1] in cs: delL.append(i)
                        for i in delL: G.Container.connections.remove(i)
                        del G.Container.nodes[
                            [i[1] for i in G.Container.nodes].index(G.Container.highlighting)
                        ]
                        G.Container.highlighting = None
            elif element.type == pygame.MOUSEBUTTONDOWN and element.button == pygame.BUTTON_RIGHT:
                dropdown()
        elif event == GO.ELAST:
            if G.Container.saved:
                if path.endswith('.elm'):
                    path = path[:-4]
                if G.Container.name != path.split('/')[1]:
                    os.remove('data/elements/'+path+'.elm')
                    path = path.split('/')[0] + '/' + G.Container.name
                    open('data/elements/'+path+'.elm', 'wb+')
                    dill.dump(G.Container.contents, open('data/elements/'+path+'.elm', 'wb+'))
    return editor(path)
