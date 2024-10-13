import pygame, dill, json, os
from importlib.resources import files

import BlazeSudio.graphics.options as GO
from BlazeSudio.graphics import Graphic
import BlazeSudio.elementGen.node_parser as np
import BlazeSudio.elementGen.types as Ts

DEFAULTFILECONTENTS = {"idea": "BLANK", "name": "New File", "version": "0.5"}

allnodes = {i: np.getCategoryNodes(i) for i in np.allCategories()}

def mouseDown(button=1):
    i = False
    while True:
        r = pygame.mouse.get_pressed(3)[button-1]
        yield ((i != r and r), r)
        i = r

def CAT(txt, front=True, bgcol=GO.CWHITE, colour=GO.CGREEN, colour2=None, filled=False, docircle=True): # Circle And Text
    t = GO.FFONT.render(txt, GO.CBLACK)
    sze = max(GO.FFONT.linesize, t.get_height())
    tocenter = (sze - t.get_height()) / 2
    sur = pygame.Surface((t.get_width() + sze + 5, sze))
    sur.fill(bgcol)
    cir = None
    if not docircle:
        sur.blit(t, (0, tocenter))
        cir = pygame.Rect(0, 0, 0, 0)
    elif front:
        cir = pygame.Rect(0, 0, sze, sze)
        pygame.draw.circle(sur, GO.CAWHITE, (sze//2, sze//2), sze//2-2)
        pygame.draw.circle(sur, colour, (sze//2, sze//2), sze//2-2, 5)
        if colour2 is not None:
            csur = pygame.Surface((sze, sze//2))
            csur.fill(GO.CAWHITE)
            pygame.draw.circle(csur, colour2, (sze//2, 0), sze//2-2, 5)
            sur.blit(csur, (0, sze//2))
        if filled:
            pygame.draw.circle(sur, GO.CGREY, (sze//2, sze//2), sze//4)
        pygame.draw.circle(sur, GO.CBLACK, (sze//2, sze//2), sze//2, 2)
        sur.blit(t, (sze + 5, tocenter))
    else:
        cir = pygame.Rect(t.get_width() + 5, 0, sze, sze)
        pygame.draw.circle(sur, GO.CAWHITE, (t.get_width() + 5 + sze//2, sze//2), sze//2-2)
        pygame.draw.circle(sur, colour, (t.get_width() + 5 + sze//2, sze//2), sze//2-2, 5)
        if colour2 is not None:
            csur = pygame.Surface((sze, sze//2))
            csur.fill(GO.CAWHITE)
            pygame.draw.circle(csur, colour2, (sze//2, 0), sze//2-2, 5)
            sur.blit(csur, (t.get_width() + 5, sze//2))
        if filled:
            pygame.draw.circle(sur, GO.CGREY, (t.get_width() + 5 + sze//2, sze//2), sze//4)
        pygame.draw.circle(sur, GO.CBLACK, (t.get_width() + 5 + sze//2, sze//2), sze//2, 2)
        sur.blit(t, (0, tocenter))
    return sur, cir

def NodeEditor(path=None, G=None):
    """
    Go edit some nodes!!!

    Args:
        path (str, optional): The path to the currently editing Node file. If it does not exist, it will be created; \
and if it is None then it will not save. Defaults to None.
        G (graphics.Graphic, optional): The Graphic screen, if not provided will make one. Defaults to None.
    """
    if G is None:
        G = Graphic()
    def dropdown():
        p = pygame.mouse.get_pos()
        while True:
            resp = G.Dropdown([i[1:-3] for i in allnodes.keys()], pos=p)
            if isinstance(resp, int) and not isinstance(resp, bool):
                resp2 = G.Dropdown(['Back']+[i.name for i in allnodes[list(allnodes.keys())[resp]]], pos=p)
                if isinstance(resp2, int) and not isinstance(resp, bool):
                    if resp2 != 0:
                        G.Container.nodes.append((p, allnodes[list(allnodes.keys())[resp]][resp2-1].copy()))
                        next(G.Container.md[0])
                        return True
                else:
                    return False
            else:
                return False
    
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
            # TODO: Better saving and loading
            if path is not None:
                if not path.endswith('.elm'):
                    path = path + '.elm'
                if not os.path.exists(path):
                    # Version: major.minor
                    dill.dump(DEFAULTFILECONTENTS, path.open('wb+'))
                # TODO: version checking and updating (not for versions less than 1.0 which is the liftoff version)
                G.Container.contents = dill.loads((files('BlazeSudio') / path+'.elm').read_bytes())
            else:
                G.Container.contents = DEFAULTFILECONTENTS
            if 'nodes' in G.Container.contents:
                G.Container.nodes = G.Container.contents['nodes']
            else:
                G.Container.nodes = []
            if 'connections' in G.Container.contents:
                G.Container.connections = G.Container.contents['connections']
            else:
                G.Container.connections = []
            G.Container.name = G.Container.contents['name']
            G.Container.highlightedIO = {}
        if event == GO.ELOADUI:
            G.Clear()
            G.add_text(G.Container.name, GO.CGREEN, GO.PCTOP, GO.FTITLE)
            G.add_button('Settings', GO.CGREEN, GO.PRTOP)
        elif event == GO.EELEMENTCLICK: # This is going to be the only button that was created
            @G.Graphic
            def settings(event, element=None, aborted=False):
                if event == GO.EFIRST:
                    G.Container.doApply = False
                elif event == GO.ELOADUI:
                    CBOT = GO.PNEW((1, 0), GO.PCBOTTOM.func)
                    RTOP = GO.PNEW((0, 1), GO.PRTOP.func)
                    LTOP = GO.PNEW((0, 1), GO.PLTOP.func)
                    G.Clear()
                    G.add_text('SETTINGS FOR NODE "%s":'%G.Container.name, GO.CGREEN, LTOP, GO.FFONT)
                    G.Container.inpname = G.add_input(LTOP, width=G.size[0]/3, resize=GO.RNONE, placeholder=G.Container.name)
                    G.add_text('SETTINGS FOR NODE EDITOR:', GO.CBLUE, RTOP, GO.FFONT)
                    G.add_empty_space(CBOT, -20, 0)
                    G.Container.go = G.add_button('Apply!', GO.CGREEN, CBOT)
                    G.Container.exit = G.add_button('Cancel', GO.CGREY, CBOT)
                elif event == GO.EELEMENTCLICK:
                    if element == G.Container.go:
                        G.Container.doApply = True
                        G.Abort()
                    elif element == G.Container.exit:
                        G.Abort()
                elif event == GO.ELAST:
                    if G.Container.doApply:
                        res = G.uids[G.Container.inpname].text
                        if res != '':
                            G.Container.name = res
                            G.Container.contents['name'] = res
            settings()
        elif event == GO.ETICK:
            lf, l = next(G.Container.md[0])
            # lf = left mouse button first press, l = left mouse button is being pressed
            
            w, h = G.size[0] / 8 * 3, G.size[1] / 8 * 3
            SideRec = pygame.Rect(8, G.size[1]-h-8, w, h)
            TouchingSide = SideRec.collidepoint(*pygame.mouse.get_pos())
            filleds = []
            if lf and not TouchingSide:
                G.Container.highlighting = None
            for p, node in G.Container.nodes:
                col = GO.CBLUE
                txt = GO.FFONT.render(node.name, GO.CBLACK)
                sur = pygame.Surface(G.size, pygame.SRCALPHA)
                sur.blit(txt, p)
                start = txt.get_height() + 5
                i = start
                mx = txt.get_width()
                for n in node.inputs:
                    name = n.name
                    if np.Mods.NoShow in n.mods:
                        continue
                    # if n.connectedto is not None and \
                    #     n.get_CT(G.Container.nodes).name in gotten and \
                    #         gotten[n.get_CT(G.Container.nodes).name] != Ts.defaults[Ts.strtypes[n.get_CT(G.Container.nodes).type]]:
                    #             name += '='+str(gotten[n.get_CT(G.Container.nodes).name])
                    # elif n.value != Ts.defaults[n.strtype] or n.type is bool:
                    #     name += ':'+str(n.value)
                    s, c = CAT(name, bgcol=col)
                    c.move_ip((p[0], i+p[1]))
                    if c.collidepoint(pygame.mouse.get_pos()):
                        filleds.append(c)
                    sur.blit(s, (p[0], i+p[1]))
                    mx = max(mx, s.get_width())
                    i += s.get_height() + 2
                    #rd = parse(n, l, lf, rd, TouchingSide)
                if node.outputs != []:
                    mx += 20
                i2 = start
                mx2 = 0
                for n in node.outputs:
                    name = n.name
                    if np.Mods.NoShow in n.mods:
                        continue
                    # if n.connectedto is not None and \
                    #     n.get_CT(G.Container.nodes).name in gotten and \
                    #         gotten[n.get_CT(G.Container.nodes).name] != Ts.defaults[Ts.strtypes[n.get_CT(G.Container.nodes).type]]:
                    #             name += '='+str(gotten[n.get_CT(G.Container.nodes).name])
                    # elif n.value != Ts.defaults[n.strtype] or n.type is bool:
                    #     name += ':'+str(n.value)
                    s, c = CAT(name, bgcol=col, front=False)
                    c.move_ip((p[0]+mx, i2+p[1]))
                    if c.collidepoint(pygame.mouse.get_pos()):
                        filleds.append(c)
                    sur.blit(s, (p[0]+mx, i2+p[1]))
                    mx2 = max(mx2, s.get_width())
                    i2 += s.get_height() + 2
                mx2 += mx
                mxhei = max(i, i2)
                r = pygame.Rect(*p, mx2+10, mxhei+10)
                pygame.draw.rect(G.WIN, col, r, border_radius=8)
                if G.Container.highlighting == node:
                    pygame.draw.rect(G.WIN, GO.CACTIVE, pygame.Rect(p[0]-15, p[1]-15, mx2+40, mxhei+40), width=10, border_radius=8)
                if G.Container.selecting is None and lf and r.collidepoint(pygame.mouse.get_pos()):
                    if not TouchingSide:
                        G.Container.highlighting = None
                    G.Container.selecting = [G.Container.nodes.index((p, node)), pygame.mouse.get_pos(), True, node]
                G.WIN.blit(sur, (0, 0))
            for i in filleds:
                G.WIN.blit(CAT('', filled=True, bgcol=col)[0], i)
            
            if not l and G.Container.selecting is not None:
                if G.Container.selecting[2]:
                    G.Container.highlighting = G.Container.selecting[3]
                G.Container.selecting = None
            
            if G.Container.selecting is not None:
                if pygame.mouse.get_pos() != G.Container.selecting[1]:
                    G.Container.selecting[2] = False
                    G.Container.nodes[G.Container.selecting[0]] = (
                        (
                            (pygame.mouse.get_pos()[0]-G.Container.selecting[1][0])+G.Container.nodes[G.Container.selecting[0]][0][0],
                            (pygame.mouse.get_pos()[1]-G.Container.selecting[1][1])+G.Container.nodes[G.Container.selecting[0]][0][1]
                        ), G.Container.nodes[G.Container.selecting[0]][1]
                    )
                    G.Container.selecting[1] = pygame.mouse.get_pos()
            
            # if isinstance(G.Container.selecting, tuple):
            #     pygame.draw.line(G.WIN, GO.CRED, G.Container.selecting[1], pygame.mouse.get_pos(), 10)
            # elif isinstance(G.Container.selecting, list):
            #     G.Container.nodes[G.Container.selecting[0]] = (
            #         (pygame.mouse.get_pos()[0]-G.Container.selecting[1][0],
            #          pygame.mouse.get_pos()[1]-G.Container.selecting[1][1]), 
            #         G.Container.nodes[G.Container.selecting[0]][1])
            
            for i in G.Container.connections:
                pygame.draw.line(G.WIN, GO.CNEW('orange'), \
                    (i[0].rect.center[0]+5, i[0].rect.center[1]+7), \
                    (i[1].rect.center[0]+5, i[1].rect.center[1]+7), 10)
            
            if G.Container.highlighting is not None:
                w, h = G.size[0] / 8 * 3, G.size[1] / 8 * 3
                node = G.Container.highlighting
                if G.Stuff['scrollsables'] == []:
                    G.Container.highlightedIO = {}
                    nopos = GO.PSTATIC(0, 0)
                    scr, scrObj1 = G.add_Scrollable(nopos, (0, 0), (0, 0))
                    h = scr.add_text(node.name, GO.CBLACK, nopos, GO.FTITLE).size[1]
                    for isinput, li in ((True, node.inputs), (False, node.outputs)): # TODO: Put inputs on the left and outputs on the right
                        if isinput:
                            h += scr.add_text('INPUTS:', GO.CBLACK, nopos, GO.FTITLE).size[1]
                        else:
                            h += scr.add_text('OUTPUTS:', GO.CBLACK, nopos, GO.FTITLE).size[1]
                        for n in li:
                            if isinput:
                                h += scr.add_text(n.name+':', GO.CBLACK, nopos).size[1]
                                e = None
                                if n.strtype == 'number':
                                    e = scr.add_num_input(nopos, font=GO.FFONT, width=10, start=n.value)
                                elif n.strtype == 'str':
                                    e = scr.add_input(nopos, font=GO.FFONT, width=GO.FFONT.winSze('c'*10)[0], start=n.value)
                                elif n.strtype == 'bool':
                                    e = scr.add_switch(nopos, default=n.value)
                                elif n.strtype == 'any':
                                    e = scr.add_input(nopos, font=GO.FFONT, width=GO.FFONT.winSze('c'*10)[0], start=str(n.value or ''))
                                if e is not None:
                                    h += e.size[1]
                                    G.Container.highlightedIO[n] = e
                            else:
                                h += scr.add_text(f'{n.name}: {n.value}', GO.CBLACK, nopos).size[1]
                    scr2, scrObj2 = G.add_Scrollable(GO.PSTATIC(SideRec.x, SideRec.y), (SideRec.w-8, SideRec.h), (SideRec.w-8, max(SideRec.h, h)), 2, True)
                    scr2.Stuff = scr.Stuff.copy()
                    scr2.stacks = scr.stacks.copy()
                    scrObj1.remove()
                    LTOP = GO.PNEW([0, 1], GO.PLTOP.func, 0, 0)
                    for sp in scr2.stacks.alls[nopos].copy():
                        e = sp.parent
                        e.G = scr2
                        e.change_pos(LTOP)
                else:
                    for io, elm in G.Container.highlightedIO.items():
                        io.value = elm.get()
            elif G.Stuff['scrollsables'] != []:
                G.Container.highlightedIO = {}
                G.Reload()
            return True
        elif event == GO.EEVENT: # When something like a button is pressed. Is passed 'element' too, but this time it is an event
            if element.type == pygame.KEYDOWN:
                if element.key == pygame.K_s and element.mod & pygame.KMOD_CTRL:
                    if path is None:
                        G.Toast('Cannot save file as file location wasn\'t specified!!')
                    else:
                        G.Toast('Saving...')
                        G.Container.contents['nodes'] = G.Container.nodes
                        G.Container.contents['connections'] = G.Container.connections
                        if not path.endswith('.elm'):
                            path = path + '.elm'
                        dill.dump(G.Container.contents, open(path, 'wb+'))
                        G.Container.saved = True
                        G.toasts = []
                        G.Toast('Saved!')
                elif element.key == pygame.K_DELETE:
                    if G.Container.highlighting is not None:
                        del G.Container.nodes[
                            [i[1] for i in G.Container.nodes].index(G.Container.highlighting)
                        ]
                        G.Container.highlighting = None
            elif element.type == pygame.MOUSEBUTTONDOWN and element.button == pygame.BUTTON_RIGHT:
                dropdown()
        elif event == GO.ELAST:
            if path is not None:
                if G.Container.saved:
                    if not path.endswith('.elm'):
                        path = path + '.elm'
                    dill.dump(G.Container.contents, open(path, 'wb+'))
    return editor(path)
