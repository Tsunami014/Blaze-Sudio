try:
    from tkinter.filedialog import askopenfilename
except ImportError as e:
    print('Sorry, the Theme Playground requires Tkinter and it could not be found.')
    raise e
from math import floor
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
    def __init__(self, parentElm, dir, pos, offset=0):
        self.parent = parentElm
        self.dir = dir
        self.pos = pos
        self.held = False
        self.offset = offset
    
    def draw(self, win):
        if self.dir == 0:
            pygame.draw.rect(win, (125, 125, 125), (self.pos+self.offset, 0, 1, win.get_height()))
        if self.dir == 1:
            pygame.draw.rect(win, (125, 125, 125), (0, self.pos+self.offset, win.get_width(), 1))
    
    def update(self, mousePos, events):
        coll = self.pos + self.offset == floor(mousePos[self.dir])
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == pygame.BUTTON_LEFT:
                if coll:
                    self.held = True
        if not pygame.mouse.get_pressed()[0]:
            self.held = False
        if self.held:
            self.pos = floor(mousePos[self.dir]) - self.offset + self.dir
        return coll

class ImageEditor(GUI.ImageViewer):
    def __init__(self, G, pos, themePart, size=(300, 300), defaultLinePoss=(None, None, None, None)):
        self.themePart = themePart
        self.theme = GUI.GLOBALTHEME.THEME
        self.lastSur = None
        self.lines = [Line(self, 0, 0), Line(self, 1, 0), Line(self, 0, 0, 1), Line(self, 1, 0, 1)]
        self.defLinePs = defaultLinePoss
        super().__init__(G, pos, pygame.Surface((0, 0)), size)
    
    def modifySur(self, sur):
        if sur.get_size() == (0, 0):
            return sur
        
        endsur = pygame.Surface((sur.get_width()+2, sur.get_height()+2), pygame.SRCALPHA)
        
        endsur.blit(sur, (1, 1))
        endsur.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)

        p = (self.lines[0].pos, self.lines[1].pos)
        endsur.blit(sur, (p[0]+1, p[1]+1), (*p, self.lines[2].pos-p[0]+1, self.lines[3].pos-p[1]+1))

        for ln in self.lines:
            ln.draw(endsur)
        
        return endsur
    
    def update(self, mousePos, events):
        part = getattr(self.theme, self.themePart)
        if part is None:
            self.sur = pygame.Surface((0, 0))
        else:
            self.sur = part.sur
        self.cache = None
        if (not self.lastSur) or self.lastSur.get_buffer().raw != self.sur.get_buffer().raw: # Because regular != doesn't work for who knows why
            self.lastSur = self.sur
            self.lines[0].pos = self.defLinePs[0] or 0
            self.lines[1].pos = self.defLinePs[1] or 0
            self.lines[2].pos = self.defLinePs[2] or self.sur.get_width()
            self.lines[3].pos = self.defLinePs[3] or self.sur.get_height()
            self.centre()
        newMP = self.unscale_pos(mousePos.pos)

        if part is not None:
            part.crop = (self.lines[0].pos, self.lines[1].pos, self.lines[2].pos-self.lines[0].pos, self.lines[3].pos-self.lines[1].pos)

        coll = False
        if (not self.G.pause) and pygame.Rect(*self.stackP(), *self.size).collidepoint(*mousePos.pos):
            for ln in self.lines:
                coll = ln.update(newMP, events) or coll
        linesHeld = any(i.held for i in self.lines)
        if linesHeld:
            self.cache = None
            prevpaused = self.G.pause
            self.G.pause = True
            super().update(mousePos, events)
            self.G.pause = prevpaused
        else:
            super().update(mousePos, events)
        if coll:
            mouse.Mouse.set(mouse.MouseState.PICK)

class ThemeProperties(GUI.PresetFrame):
    def __init__(self, G, pos: GO.P___, themePart):
        self.themePart = themePart
        super().__init__(G, pos)
    
    def _init_objects(self):
        self.layers[0].add('main')
        PRTOP = GO.PNEW((1, 0), (0, 1))
        def change():
            def ask():
                self.pause = True
                newf = askopenfilename(filetypes=[('Image file', '*.png *.jpg *.jpeg *.bmp *.gif')])
                if newf:
                    setattr(GUI.GLOBALTHEME.THEME, self.themePart, GUI.Image(newf))
                    t1.set(newf)
                    im.defLinePs = (None, None, None, None)
                    self.themeInps[0].set(1)
                    self.themeInps[1].set(1)
                    im.active = True
                    self.fitObjects()
                self.pause = False
            Thread(target=ask, daemon=True).start()
            return ReturnState.DONTCALL
        def unset():
            setattr(GUI.GLOBALTHEME.THEME, self.themePart, None)
            t1.set('None')
            im.active = False
            self.fitObjects()
            return ReturnState.DONTCALL
        b1 = GUI.Button(self, PRTOP, GO.CORANGE, 'Change the image source 🔁', func=change, allowed_width=300)
        b2 = GUI.Button(self, PRTOP, GO.CRED, 'Unset the image source ❎', func=unset, allowed_width=300)
        p = getattr(GUI.GLOBALTHEME.THEME, self.themePart)
        if p is None:
            n = 'None'
        else:
            n = p.fname
        t1 = GUI.Text(self, PRTOP, n, allowed_width=600, leftrightweight=GO.SWRIGHT)
        im = ImageEditor(self, PRTOP, self.themePart, size=(400, 400))
        im.active = n is not None
        if p is None:
            scales = (1, 1)
        else:
            scales = p.scale
            im.defLinePs = (*p.crop[:2], p.crop[2]-p.crop[0], p.crop[3]-p.crop[1])

        g = GUI.GridLayout(self, PRTOP, leftrightWeight=GO.SWLEFT)
        n1 = GUI.NumInputBox(g, g.LP, 100, start=scales[0], placeholdOnNum=None, max=1000, min=-1000)
        n2 = GUI.NumInputBox(g, g.LP, 100, start=scales[1], placeholdOnNum=None, max=1000, min=-1000)
        g.grid = [
            [GUI.Text(g, g.LP, 'Horizontal scale: '), n1],
            [GUI.Text(g, g.LP, 'Vertical scale: '), n2]
        ]

        self.themeInps = [
            n1,
            n2,
        ]
        self['main'].extend([
            b1,
            b2,
            t1,
            im,
            g,
        ])
    
    def _update(self, mousePos, events):
        p = getattr(GUI.GLOBALTHEME.THEME, self.themePart)
        if p is not None:
            p.scale = (
                self.themeInps[0].get(),
                self.themeInps[1].get()
            )
        return super()._update(mousePos, events)

class BaseThemeTest:
    NAME = None
    THEMENAME = None

    def __new__(cls, force_create=False):
        if force_create:
            return super().__new__(cls)
        cls(True).screen()
    
    @G.Screen
    def screen(event, self, element=None, aborted=False):
        if event == GO.ELOADUI:
            G.Clear()
            self.main = self.load_main()
            G['Main'].append(self.main)
            G['Main'].append(GUI.Text(G, GO.PCTOP, self.NAME.upper(), font=GO.FTITLE))
            LTOP = GO.PNEW((0, 0), (0, 1))
            G['Left'].append(GUI.Text(G, LTOP, 'Sample %s properties'%self.NAME.lower(), font=GO.FTITLE))
            G['Left'].extend(self.load_props(LTOP))
            RTOP = GO.PNEW((1, 0), (0, 1))
            G['Right'].extend([
                GUI.Text(G, RTOP, self.NAME+' theme properties', font=GO.FTITLE),
                ThemeProperties(G, RTOP, self.THEMENAME),
            ])
        elif event == GO.ETICK:
            self.tick(G['Left'][1:])
    
    def load_main(self):
        return None

    def load_props(self, LTOP):
        return []
    
    def tick(self, props):
        pass

class TextTest(BaseThemeTest):
    NAME = 'Text'
    THEMENAME = 'BUTTON' # TODO: Add theme for text (fonts)
    def load_main(self):
        return GUI.Text(G, GO.PCCENTER, 'Hello!')
    
    def load_props(self, LTOP):
        return [
            GUI.Text(G, LTOP, 'Text'),
            GUI.InputBox(G, LTOP, 300, GO.RHEIGHT, starting_text='Sample'),
            GUI.Text(G, LTOP, 'Colour of text'),
            GUI.ColourPickerBTN(G, LTOP, default=(0, 0, 0)),
            GUI.Text(G, LTOP, 'Render dash?'),
            GUI.Switch(G, LTOP, default=True),
            GUI.Text(G, LTOP, 'leftrightweight'),
            GUI.DropdownButton(G, LTOP, ['Left', 'Mid', 'Right'], default=1),
            GUI.Text(G, LTOP, 'updownweight'),
            GUI.DropdownButton(G, LTOP, ['Top', 'Mid', 'Bottom'], default=1),
            # TODO: Font
            GUI.Text(G, LTOP, 'Allowed width'),
            GUI.NumInputBox(G, LTOP, 300, GO.RHEIGHT, start=0, min=0, placeholdOnNum=None),
        ]
    
    def tick(self, props):
        self.main.col = props[3].get()
        lr = [GO.SWLEFT, GO.SWMID, GO.SWRIGHT][props[7].get(True)]
        ud = [GO.SWTOP, GO.SWMID, GO.SWBOT][props[9].get(True)]
        self.main.set(props[1].get(), 
                      renderdash=props[5].get(), 
                      leftrightweight=lr, 
                      updownweight=ud, 
                      allowed_width=(props[11].get() or None)
        )

class ButtonTest(TextTest):
    NAME = 'Button'
    THEMENAME = 'BUTTON'
    def load_main(self):
        return GUI.Button(G, GO.PCCENTER, GO.CRED, 'Hello!')
    
    def load_props(self, LTOP):
        return [
            *super().load_props(LTOP),
            GUI.Text(G, LTOP, 'Colour of button'),
            GUI.ColourPickerBTN(G, LTOP),
            GUI.Text(G, LTOP, 'On hover enlarge'),
            GUI.NumInputBox(G, LTOP, 100, GO.RHEIGHT, start=5, min=0, placeholdOnNum=None),
            GUI.Text(G, LTOP, 'Spacing'),
            GUI.NumInputBox(G, LTOP, 100, GO.RHEIGHT, start=2, min=0, placeholdOnNum=None),
        ]
    
    def tick(self, props):
        self.main.cols = {'BG': props[-5].get(), 'TXT': props[3].get()}
        self.main.OHE = props[-3].get()
        self.main.spacing = props[-1].get()
        super().tick(props)

@G.Screen
def test(event, element=None, aborted=False):
    if event == GO.ELOADUI:
        G.Clear()
        G['Main'].append(GUI.Text(G, GO.PCTOP, 'THEME EDITOR', font=GO.FTITLE))
        rainbow = GO.CRAINBOW()
        LTOP = GO.PNEW((0, 0), (0, 1))
        G['Main'].extend([
            GUI.Button(G, LTOP, next(rainbow), 'Test text', func=TextTest),
            GUI.Button(G, LTOP, next(rainbow), 'Test button', func=ButtonTest),
        ])

test()
