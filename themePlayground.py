try:
    from tkinter.filedialog import askopenfilename
except ImportError as e:
    print('Sorry, the Theme Playground requires Tkinter and it could not be found.')
    raise e
from math import ceil, floor
from BlazeSudio.graphics import Graphic, mouse, GUI, options as GO
from BlazeSudio.graphics.GUI.base import ReturnState
from threading import Thread
import pygame
G = Graphic()
G.layers[0].add_many([
    'Main',
    'Left',
    'Right'
])

class Line:
    def __init__(self, parentElm, dir, pos):
        self.parent = parentElm
        self.dir = dir
        self.pos = pos
        self.held = False
        self.last_pos = None
    
    def draw(self, win):
        if self.dir == 0:
            pygame.draw.rect(win, (125, 125, 125), (self.pos-1, 0, 2, win.get_height()))
        if self.dir == 1:
            pygame.draw.rect(win, (125, 125, 125), (0, self.pos-1, win.get_width(), 2))
    
    def update(self, mousePos, events):
        coll = abs(mousePos[self.dir] - self.pos) <= 1
        if coll:
            mouse.Mouse.set(mouse.MouseState.PICK)
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == pygame.BUTTON_LEFT:
                if coll:
                    self.held = True
        if not pygame.mouse.get_pressed()[0]:
            self.held = False
        if self.held:
            self.pos += floor(mousePos[self.dir])-self.last_pos
        self.last_pos = floor(mousePos[self.dir])

class ImageEditor(GUI.ImageViewer):
    def __init__(self, G, pos, themePart, size=(300, 300), defaultLinePoss=(None, None, None, None)):
        self.themePart = themePart
        self.theme = GUI.GLOBALTHEME.THEME
        self.lastSur = None
        self.lines = [Line(self, 0, 0), Line(self, 1, 0), Line(self, 0, 0), Line(self, 1, 0)]
        self.defLinePs = defaultLinePoss
        super().__init__(G, pos, pygame.Surface((0, 0)), size)
    
    def update(self, mousePos, events):
        part = getattr(self.theme, self.themePart)
        if part is None:
            self.sur = pygame.Surface((0, 0))
        else:
            self.sur = part.sur
        if self.lastSur != self.sur:
            self.lastSur = self.sur
            self.centre()
            self.lines[0].pos = self.defLinePs[0] or 0
            self.lines[1].pos = self.defLinePs[1] or 0
            self.lines[2].pos = self.defLinePs[2] or self.sur.get_width()
            self.lines[3].pos = self.defLinePs[3] or self.sur.get_height()
        ns = self.sur.copy()
        newMP = self.unscale_pos(mousePos)
        for ln in self.lines:
            ln.draw(ns)
        
        endsur = pygame.Surface(ns.get_size(), pygame.SRCALPHA)
        endsur.blit(ns, (0, 0))
        endsur.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)
        p = (self.lines[0].pos, self.lines[1].pos)
        endsur.blit(ns, p, (*p, self.lines[2].pos-p[0], self.lines[3].pos-p[1]))

        if part is not None:
            part.crop = (self.lines[0].pos, self.lines[1].pos, self.lines[2].pos-self.lines[0].pos, self.lines[3].pos-self.lines[1].pos)

        prevpaused = self.G.pause
        self.G.pause = self.G.pause or any(i.held for i in self.lines)
        super().update(mousePos, events, endsur)
        self.G.pause = prevpaused
        if (not self.G.pause) and pygame.Rect(*self.stackP(), *self.size).collidepoint(mousePos):
            for ln in self.lines:
                ln.update(newMP, events)

def changeTheme(position, themePart):
    def change():
        def ask():
            G.pause = True
            newf = askopenfilename(filetypes=[('Image file', '*.png *.jpg *.jpeg *.bmp *.gif')])
            if newf:
                setattr(GUI.GLOBALTHEME.THEME, themePart, GUI.Image(newf))
                t1.set(newf)
                im.defLinePs = (None, None, None, None)
                G.Container.themeInps[0].set(1)
                G.Container.themeInps[1].set(1)
                im.active = True
            G.pause = False
        Thread(target=ask, daemon=True).start()
        return ReturnState.DONTCALL
    def unset():
        setattr(GUI.GLOBALTHEME.THEME, themePart, None)
        t1.set('None')
        im.active = False
        return ReturnState.DONTCALL
    b1 = GUI.Button(G, position, GO.CORANGE, 'Change the image source 🔁', func=change, allowed_width=300)
    b2 = GUI.Button(G, position, GO.CRED, 'Unset the image source ❎', func=unset, allowed_width=300)
    p = getattr(GUI.GLOBALTHEME.THEME, themePart)
    if p is None:
        n = 'None'
    else:
        n = p.fname
    t1 = GUI.Text(G, position, n, allowed_width=300)
    im = ImageEditor(G, position, themePart)
    im.active = n is not None
    if p is None:
        scales = (1, 1)
    else:
        scales = p.scale
        im.defLinePs = (*p.crop[:2], p.crop[2]-p.crop[0], p.crop[3]-p.crop[1])

    G.Container.themeInps = [
        GUI.NumInputBox(G, position, 100, start=scales[0], placeholdOnNum=None),
        GUI.NumInputBox(G, position, 100, start=scales[1], placeholdOnNum=None)
    ]
    return [
        b1,
        b2,
        t1,
        im,
        *G.Container.themeInps
    ]

def changeThemeTick(themePart):
    p = getattr(GUI.GLOBALTHEME.THEME, themePart)
    if p is not None:
        p.scale = (
            G.Container.themeInps[0].get() or 1,
            G.Container.themeInps[1].get() or 1
        )

@G.Screen
def testButton(event, element=None, aborted=False):
    if event == GO.ELOADUI:
        G.Clear()
        G.Container.MainBtn = GUI.Button(G, GO.PCCENTER, GO.CRED, 'Hello!')
        G['Main'].append(G.Container.MainBtn)
        LTOP = GO.PNEW((0, 0), (0, 1))
        G['Left'].extend([
            GUI.Text(G, LTOP, 'Sample button properties', font=GO.FTITLE),
            GUI.Text(G, LTOP, 'Colour of button'),
            GUI.ColourPickerBTN(G, LTOP),
            GUI.Text(G, LTOP, 'Colour of text'),
            GUI.ColourPickerBTN(G, LTOP, default=(0, 0, 0)),
            GUI.Text(G, LTOP, 'Text in button'),
            GUI.InputBox(G, LTOP, 100, GO.RHEIGHT, starting_text='Sample'),
            GUI.Text(G, LTOP, 'Allowed width'),
            GUI.NumInputBox(G, LTOP, 100, GO.RHEIGHT, start=0, min=0, placeholdOnNum=None),
            GUI.Text(G, LTOP, 'On hover enlarge'),
            GUI.NumInputBox(G, LTOP, 100, GO.RHEIGHT, start=5, min=0, placeholdOnNum=None),
            GUI.Text(G, LTOP, 'Spacing'),
            GUI.NumInputBox(G, LTOP, 100, GO.RHEIGHT, start=2, min=0, placeholdOnNum=None),
        ])
        RTOP = GO.PNEW((1, 0), (0, 1))
        G['Right'].extend([
            GUI.Text(G, RTOP, 'Button theme properties', font=GO.FTITLE),
            *changeTheme(RTOP, 'BUTTON')
        ])
    elif event == GO.ETICK:
        G.Container.MainBtn.cols = {'BG': G['Left'][2].get(), 'TXT': G['Left'][4].get()}
        G.Container.MainBtn.set(G['Left'][6].get(), allowed_width=(G['Left'][8].get() or None))
        G.Container.MainBtn.OHE = G['Left'][10].get()
        G.Container.MainBtn.spacing = G['Left'][12].get()
        changeThemeTick('BUTTON')
    # elif event == GO.EELEMENTCLICK:
    #     GUI.GLOBALTHEME.THEME.BUTTON = element.get()

@G.Screen
def test(event, element=None, aborted=False):
    if event == GO.ELOADUI:
        G.Clear()
        G['Main'].append(GUI.Text(G, GO.PCTOP, 'THEME EDITOR', font=GO.FTITLE))
        rainbow = GO.CRAINBOW()
        G['Main'].extend([
            GUI.Button(G, GO.PLTOP, next(rainbow), 'Test button', func=testButton),
        ])

test()
