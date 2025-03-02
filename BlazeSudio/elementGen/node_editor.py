import pygame

from BlazeSudio.elementGen.image import Image
import BlazeSudio.graphics.options as GO
from BlazeSudio.graphics import GUI, Screen
import BlazeSudio.elementGen.node_parser as np
import BlazeSudio.elementGen.node_file as nf

allnodes = {i: np.getCategoryNodes(i) for i in np.allCategories()}

def mouseDown(button=1):
    i = False
    while True:
        r = pygame.mouse.get_pressed(3)[button-1]
        yield ((i != r and r), r)
        i = r

class settings(Screen):
    def __init__(self, name):
        self.name = name
        self.doApply = False
        super().__init__()
    
    def _LoadUI(self):
        self.layers[0].add_many([
            'NodeSettings',
            'EditorSettings',
            'SettingsBottom'
        ])
        CBOT = GO.PNEW((0.5, 1), (1, 0), (True, False))
        RTOP = GO.PNEW((1, 0), (0, 1))
        LTOP = GO.PNEW((0, 0), (0, 1))
        self.Clear()
        self['NodeSettings'].extend([
            GUI.Text(LTOP, 'SETTINGS FOR NODE "%s":'%self.name, GO.CGREEN),
            GUI.InputBox(LTOP, self.size[0]/3, GO.RNONE, starting_text=self.name)
        ])
        self['EditorSettings'].extend([
            GUI.Text(RTOP, 'SETTINGS FOR NODE EDITOR:', GO.CBLUE)
        ])
        self['SettingsBottom'].append(GUI.Empty(CBOT, (-20, 0)))
        self.ApplyBtn = GUI.Button(CBOT, GO.CGREEN, 'Apply!')
        self['SettingsBottom'].extend([
            self.ApplyBtn,
            GUI.Button(CBOT, GO.CGREY, 'Cancel'),
        ])
    def _ElementClick(self, obj):
        if obj == self.ApplyBtn:
            self.doApply = True
        self.Abort()
    def _Last(self, aborted):
        if self.doApply:
            return [e.get() for e in self['NodeSettings'][1:]], \
                    [e.get() for e in self['EditorSettings'][1:]]

class NodeEditor(Screen):
    def __init__(self, path=None):
        """
        Go edit some nodes!!!

        Args:
            path (str, optional): The path to the currently editing Node file. If it does not exist, it will be created; \
    and if it is None then it will not save. Defaults to None.
        """
        self.saved = False
        self.md = mouseDown() # Left mouse button
        self.selecting = None
        self.highlighting = None
        if path is not None:
            if not path.endswith('.elm'):
                self.path = path + '.elm'
        else:
            self.path = None
        self.file = nf.NodeFile(np.getAllNodes(), self.path)
        self.nodes = self.file.nodes
        self.connections = self.file.conns
        self.name = self.file.name
        super().__init__()
    
    def CAT(self, txt, front=True, bgcol=GO.CWHITE, colour=GO.CGREEN, colour2=None, filled=False, docircle=True): # Circle And Text
        t = GO.FREGULAR.render(txt, GO.CBLACK)
        sze = max(GO.FREGULAR.linesize, t.get_height())
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

    def dropdown(self, p=None):
        p = p or pygame.mouse.get_pos()
        def nxt(resp):
            def nxt2(resp2):
                if resp2 is not None:
                    if resp2 == 0:
                        self.dropdown(p)
                    else:
                        self.nodes.append((p, allnodes[list(allnodes.keys())[resp]][resp2-1].copy()))
                        next(self.md)
            if resp is not None:
                self['Dropdowns'].append(GUI.Dropdown(p, ['Back']+[i.name for i in allnodes[list(allnodes.keys())[resp]]], func=nxt2))
        
        self['Dropdowns'].append(GUI.Dropdown(p, [i[1:-3] for i in allnodes.keys()], func=nxt))
    
    def deleteConn(self, conn):
        self.connections.pop(conn, None)
        for c in self.connections.copy():
            if self.connections[c] == conn:
                self.connections.pop(c)
    
    def _LoadUI(self):
        self.Clear()
        self.layers[0].add_many([
            'scrollsables',
            'mainUI',
            'Toasts',
            'Dropdowns',

            'NodeSettings',
            'EditorSettings',
            'SettingsBottom'
        ])
        self.settingsBtn = GUI.Button(GO.PRTOP, GO.CGREEN, 'Settings')
        self['mainUI'].extend([
            GUI.Text(GO.PCTOP, '# '+self.name, GO.CGREEN),
            self.settingsBtn
        ])
    
    def _ElementClick(self, obj): # This is going to be the only button that was created
        if obj == self.settingsBtn:
            self.name = settings(self.name)()[0][0]
            self.Reload()
    
    def _Tick(self):
        lf, l = next(self.md)
        # lf = left mouse button first press, l = left mouse button is being pressed
        
        w, h = self.size[0] / 8 * 3, self.size[1] / 8 * 3
        SideRec = pygame.Rect(8, self.size[1]-h-8, w, h)
        TouchingSide = SideRec.collidepoint(*pygame.mouse.get_pos())
        dragging = self.selecting is not None and self.selecting[0]
        filleds = []
        nodePoss = {}
        if lf and not TouchingSide:
            self.highlighting = None
        for p, node in self.nodes:
            col = GO.CBLUE
            txt = GO.FREGULAR.render(node.name, GO.CBLACK)
            sur = pygame.Surface(self.size, pygame.SRCALPHA)
            sur.blit(txt, p)
            start = txt.get_height() + 5
            i = start
            mx = txt.get_width()
            for n in node.inputs:
                name = n.name
                if np.Mods.NoNode in n.mods:
                    continue
                s, c = self.CAT(name, bgcol=col)
                c.move_ip((p[0], i+p[1]))
                nodePoss[(node, n)] = c
                if (not dragging) and c.collidepoint(pygame.mouse.get_pos()):
                    if self.selecting is None or self.selecting[1].canAccept(n):
                        filleds.append((c, n))
                        if lf:
                            self.deleteConn((node, n))
                            self.selecting = [False, n, node, c]
                sur.blit(s, (p[0], i+p[1]))
                mx = max(mx, s.get_width())
                i += s.get_height() + 2
                #rd = parse(n, l, lf, rd, TouchingSide)
            if node.outputs != []:
                mx += 20
            i2 = start
            mx2 = 0
            outs = node.run(self.connections)
            surs = []
            idx = 0
            for n in node.outputs:
                name = n.name
                if np.Mods.NoNode in n.mods:
                    continue
                if isinstance(outs[idx], (tuple, Image)):
                    name = ''
                else:
                    if outs[idx] and np.Mods.LeaveName not in n.mods or n.type is bool:
                        if np.Mods.ShowEqual in n.mods:
                            name = f'{name}: {outs[idx]}'
                        else:
                            if isinstance(outs[idx], float) and int(outs[idx]) == float(outs[idx]):
                                name = str(int(outs[idx]))
                            else:
                                name = str(outs[idx])
                s, c = self.CAT(name, bgcol=col, front=False)
                c.move_ip((p[0]+mx, i2+p[1]))
                if isinstance(outs[idx], tuple):
                    c2 = c.copy()
                    c.move_ip(c.width, 0)
                    cols = pygame.Surface((c2.w*2+5, c2.h), pygame.SRCALPHA)
                    pygame.draw.rect(cols, outs[idx], (0, 0, c2.w, c2.h), border_radius=8)
                    pygame.draw.rect(cols, (0, 0, 0), (0, 0, c2.w, c2.h), border_radius=8, width=2)
                    cols.blit(s, (c2.w, 0))
                    s = cols
                elif isinstance(outs[idx], Image):
                    c2 = c.copy()
                    c.move_ip(c.width, 0)
                    news = pygame.Surface((c2.w*2+5, c2.h), pygame.SRCALPHA)
                    news.blit(pygame.transform.scale(outs[idx].to_pygame(), (c2.w, c2.h)), (0, 0))
                    news.blit(s, (c2.w, 0))
                    s = news
                nodePoss[(node, n)] = c
                if (not dragging) and c.collidepoint(pygame.mouse.get_pos()):
                    if self.selecting is None or self.selecting[1].canAccept(n):
                        filleds.append((c, n))
                        if lf:
                            self.selecting = [False, n, node, c]
                sur.blit(s, (p[0]+mx, i2+p[1]))
                mx2 = max(mx2, s.get_width())
                i2 += s.get_height() + 2
                idx += 1
            mx2 += mx
            mxhei = max(i, i2)
            r = pygame.Rect(*p, mx2+10, mxhei+10)
            pygame.draw.rect(self.WIN, col, r, border_radius=8)
            for s in surs:
                self.WIN.blit(s[0], s[1])
            if self.highlighting == node:
                pygame.draw.rect(self.WIN, GO.CACTIVE, pygame.Rect(p[0]-15, p[1]-15, mx2+40, mxhei+40), width=10, border_radius=8)
            if self.selecting is None and lf and r.collidepoint(pygame.mouse.get_pos()):
                if not TouchingSide:
                    self.highlighting = None
                self.selecting = [True, self.nodes.index((p, node)), pygame.mouse.get_pos(), True, node]
            self.WIN.blit(sur, (0, 0))
        for i in filleds:
            self.WIN.blit(self.CAT('', filled=True, bgcol=col)[0], i[0])
        
        if not l and self.selecting is not None:
            if self.selecting[0]:
                if self.selecting[3]:
                    self.highlighting = self.selecting[4]
            else:
                if filleds != []:
                    top = filleds[0]
                    connFrom = (top[1].parent, top[1])
                    connTo = (self.selecting[2], self.selecting[1])
                    if not self.selecting[1].isinput:
                        connFrom, connTo = connTo, connFrom
                    self.connections[connTo] = connFrom
            self.selecting = None
        
        if self.selecting is not None and self.selecting[0]:
            if pygame.mouse.get_pos() != self.selecting[2]:
                self.selecting[3] = False
                self.nodes[self.selecting[1]] = (
                    (
                        (pygame.mouse.get_pos()[0]-self.selecting[2][0])+self.nodes[self.selecting[1]][0][0],
                        (pygame.mouse.get_pos()[1]-self.selecting[2][1])+self.nodes[self.selecting[1]][0][1]
                    ), self.nodes[self.selecting[1]][1]
                )
                self.selecting[2] = pygame.mouse.get_pos()
        elif self.selecting is not None and not self.selecting[0]:
            pos1 = self.selecting[3].center
            pos2 = pygame.mouse.get_pos()
            pygame.draw.circle(self.WIN, GO.CRED, pos1, 5)
            pygame.draw.circle(self.WIN, GO.CRED, pos2, 5)
            pygame.draw.line(self.WIN, GO.CRED, pos1, pos2, 10)
        
        col = GO.CORANGE
        for i in self.connections:
            pygame.draw.circle(self.WIN, col, nodePoss[i].center, 5)
            pygame.draw.circle(self.WIN, col, nodePoss[self.connections[i]].center, 5)
            pygame.draw.line(self.WIN, col, \
                nodePoss[i].center, nodePoss[self.connections[i]].center, 10)
        
        if self.highlighting is not None:
            w, h = self.size[0] / 8 * 3, self.size[1] / 8 * 3
            node = self.highlighting
            replaceOuts = False
            if self['scrollsables'] == []:
                scr = GUI.ScrollableFrame(GO.PSTATIC(SideRec.x, SideRec.y), (SideRec.w-8, SideRec.h), (0, 0))
                self['scrollsables'].append(scr)
                scr.layers[0].add_many([
                    'Inputs',
                    'Outputs',
                    'Titles'
                ])
                LTOP = GO.PNEW((0, 0), (0, 1))
                def parseIn(n):
                    e1 = GUI.Text(LTOP, n.name+':')
                    e = None
                    if n.strtype == 'number':
                        e = GUI.NumInputBox(LTOP, 10, font=GO.FREGULAR, start=n.value, placeholdOnNum=None)
                    elif n.strtype == 'str':
                        e = GUI.InputBox(LTOP, GO.FREGULAR.winSze('c'*10)[0], font=GO.FREGULAR, start=n.value, placeholdOnNum=None)
                    elif n.strtype == 'bool':
                        e = GUI.Switch(LTOP, default=n.value)
                    elif n.strtype == 'colour':
                        e = GUI.ColourPickerBTN(LTOP)
                        e.set(*n.value)
                    elif n.strtype == 'any':
                        e = GUI.InputBox(LTOP, GO.FREGULAR.winSze('c'*10)[0], font=GO.FREGULAR, starting_text=str(n.value or ''))
                    if e is None:
                        return ()
                    return (e1, e)
                def parseOut(n):
                    if n.strtype == 'image':
                        return GUI.Static(LTOP, n.value.to_pygame())
                    else:
                        return GUI.Text(LTOP, '')

                # TODO: Put inputs on the left and outputs on the right
                scr['Titles'].append(GUI.Empty(LTOP, (10, 10)))
                scr['Titles'].append(GUI.Text(LTOP, '## '+node.name))
                ins = [i for i in node.inputs if np.Mods.NoSidebar not in i.mods]
                if ins != []:
                    scr['Titles'].append(GUI.Text(LTOP, '# INPUTS:'))
                    scr['Inputs'].extend([
                        i for n in ins for i in parseIn(n)
                    ])
                os = [i for i in node.outputs if np.Mods.NoSidebar not in i.mods]
                if os != []:
                    scr['Titles'].append(GUI.Text(LTOP, '# OUTPUTS:'))
                    replaceOuts = True
                    scr['Outputs'].extend([
                        parseOut(n) for n in os
                    ])
                scr.sizeOfScreen = (SideRec.w-8, max(SideRec.h, sum(i.size[1] for i in scr.get())))
            else:
                scr = self['scrollsables'][0]
                for elm, io in zip(scr['Inputs'][1::2], node.inputs):
                    if io.value != elm.get():
                        io.value = elm.get()
                        replaceOuts = True
            if replaceOuts:
                outs = node.run(self.connections)
                for i in range(len(scr["Outputs"])):
                    oio = node.outputs[i]
                    otxt = scr["Outputs"][i]
                    if np.Mods.NoSidebar in oio.mods:
                        otxt.set('')
                    else:
                        val = outs[i]
                        if isinstance(val, Image):
                            otxt.set(val.to_pygame())
                        else:
                            if isinstance(val, float) and int(val) == float(val):
                                val = int(val)
                            otxt.set(f'{oio.name}: {val}')
                    
        elif self['scrollsables'] != []:
            self.Reload()
    
    def _Event(self, event): # When something like a button is pressed.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:
                if self.path is None:
                    self['Toasts'].append(GUI.Toast('Cannot save file as file location wasn\'t specified!!', GO.CRED))
                else:
                    self['Toasts'].append(GUI.Toast('Saving...', GO.CORANGE))
                    self.file.nodes = self.nodes
                    self.file.conns = self.connections
                    self.file.name = self.name
                    if not self.path.endswith('.elm'):
                        self.path = self.path + '.elm'
                    self.file.save(self.path)
                    self.saved = True
                    self['Toasts'].append(GUI.Toast('Saved!', GO.CGREEN))
            elif event.key == pygame.K_DELETE:
                if self.highlighting is not None:
                    for c in self.connections.copy():
                        if self.connections[c][0] == self.highlighting or c[0] == self.highlighting:
                            self.connections.pop(c)
                    del self.nodes[
                        [i[1] for i in self.nodes].index(self.highlighting)
                    ]
                    self.highlighting = None
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            self.dropdown()
    
    def _Last(self, aborted):
        if self.path is not None:
            if self.saved:
                self.file.nodes = self.nodes
                self.file.conns = self.connections
                self.file.name = self.name
                if not self.path.endswith('.elm'):
                    self.path = self.path + '.elm'
                self.file.save(self.path)
