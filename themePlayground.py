try:
    from tkinter.filedialog import askopenfilename
except ImportError as e:
    print('Sorry, the Theme Playground requires Tkinter and it could not be found.')
    raise e
from BlazeSudio.graphics import Graphic, GUI, options as GO
from BlazeSudio.graphics.GUI.base import ReturnState
from threading import Thread
import pygame
G = Graphic()
G.layers[0].add_many([
    'Main',
    'Left',
    'Right'
])

class ImageEditor(GUI.ImageViewer):
    def __init__(self, G, pos, themePart, size=(300, 300)):
        self.themePart = themePart
        self.theme = GUI.GLOBALTHEME.THEME
        self.lastSur = None
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
        ns = self.sur.copy()
        #pygame.draw.circle(ns, GO.CBLACK, self.unscale_pos(mousePos), 5)
        #pygame.draw.line(ns, GO.CBLACK, (0, self.unscale_pos(mousePos)[1]), (ns.get_width(), self.unscale_pos(mousePos)[1]), 5)
        super().update(mousePos, events, ns)

def changeTheme(position, themePart):
    def change():
        def ask():
            G.pause = True
            newf = askopenfilename(filetypes=[('Image file', '*.png *.jpg *.jpeg *.bmp *.gif')])
            if newf:
                setattr(GUI.GLOBALTHEME.THEME, themePart, GUI.Image(newf))
                t1.set(newf)
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
    n = getattr(GUI.GLOBALTHEME.THEME, themePart)
    if n is None:
        n = 'None'
    else:
        n = n.fname
    t1 = GUI.Text(G, position, n, allowed_width=300)
    im = ImageEditor(G, position, themePart)
    im.active = n is not None
    return [
        b1,
        b2,
        t1,
        im
    ]

@G.Screen
def testButton(event, element=None, aborted=False):
    if event == GO.ELOADUI:
        G.Clear()
        G.Container.MainBtn = GUI.Button(G, GO.PCCENTER, GO.CRED, 'Hello!')
        G['Main'].append(G.Container.MainBtn)
        LTOP = GO.PNEW([0, 1], GO.PLTOP.func, 0, 0)
        G['Left'].extend([
            GUI.Text(G, LTOP, 'Sample button properties', font=GO.FTITLE),
            GUI.Text(G, LTOP, 'Colour of button'),
            GUI.ColourPickerBTN(G, LTOP),
            GUI.Text(G, LTOP, 'Colour of text'),
            GUI.ColourPickerBTN(G, LTOP, default=(0, 0, 0)),
            GUI.Text(G, LTOP, 'Text in button'),
            GUI.InputBox(G, LTOP, 100, GO.RHEIGHT, starting_text='Sample'),
            GUI.Text(G, LTOP, 'Allowed width'),
            GUI.NumInputBox(G, LTOP, 100, GO.RHEIGHT, start=0, min=0),
            GUI.Text(G, LTOP, 'On hover enlarge'),
            GUI.NumInputBox(G, LTOP, 100, GO.RHEIGHT, start=5, min=0),
            GUI.Text(G, LTOP, 'Spacing'),
            GUI.NumInputBox(G, LTOP, 100, GO.RHEIGHT, start=2, min=0),
        ])
        RTOP = GO.PNEW([0, 1], GO.PRTOP.func, 0, 0)
        G['Right'].extend([
            GUI.Text(G, RTOP, 'Button theme properties', font=GO.FTITLE),
            *changeTheme(RTOP, 'BUTTON')
        ])
    elif event == GO.ETICK:
        G.Container.MainBtn.cols = {'BG': G['Left'][2].get(), 'TXT': G['Left'][4].get()}
        G.Container.MainBtn.set(G['Left'][6].get(), allowed_width=(G['Left'][8].get() or None))
        G.Container.MainBtn.OHE = G['Left'][10].get()
        G.Container.MainBtn.spacing = G['Left'][12].get()
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
