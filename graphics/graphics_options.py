import pygame
import pygame.freetype
from string import printable

# Colours
CTRANSPARENT = (255, 255, 255, 1)
CWHITE = (255, 255, 255)
CAWHITE = (200, 200, 200)
CGREEN = (60, 200, 100)
CRED = (255, 60, 100)
CBLUE = (60, 100, 255)
CBLACK = (0, 0, 0)
CYELLOW = (255, 200, 50)
CGREY = (125, 125, 125)
def CNEW(name):
    c = pygame.color.Color(name)
    return (c.r, c.g, c.b)
CINACTIVE = CNEW('lightskyblue3')
CACTIVE = CNEW('dodgerblue2')

def CRAINBOW():
    l = [
        CRED,
        CYELLOW,
        CGREEN,
        CBLUE,
        CBLACK,
        CGREY
    ]
    while True:
        for i in l: yield i

# Fonts
class FNEW:
    def __init__(self, name, size, bold=False, italic=False):
        self.font = pygame.font.SysFont(name, size, bold, italic)
        self.emojifont = pygame.freetype.SysFont('segoeuisymbol', size, bold, italic)
    def render(self, txt, col):
        if txt == '':
            return pygame.Surface((0, 0))
        parts = []
        part = ''
        prtable = None
        for i in list(txt)+[None]:
            if i is not None:
                isprt = (i in printable)
            else:
                isprt = not prtable # Assuming it has been set with something that is an actual character
            if prtable is None:
                prtable = isprt
            if isprt != prtable and i != ' ':
                if prtable:
                    parts.append(self.font.render(part, 1, col))
                else:
                    parts.append(self.emojifont.render(part, col)[0])
                part = ''
                if i is not None:
                    prtable = isprt
            if i is not None:
                part += i
        sze = (sum([i.get_width() for i in parts]), max([i.get_height() for i in parts]))
        sur = pygame.Surface(sze).convert_alpha()
        sur.fill((255, 255, 255, 1))
        curx = 0
        for i in parts:
            sur.blit(i, (curx, (sze[1]-i.get_height())*0.5))
            curx += i.get_width()
        return sur
    
    def size(self, txt):
        return self.render(txt, (0, 0, 0)).get_size()
    
    def __getattr__(self, __name):
        return getattr(self.font, __name)

FTITLE = FNEW('Comic Sans MS', 64, True)
FCODEFONT = FNEW('Lucida Sans Typewriter', 16)
FFONT = FNEW(None, 52)
FSMALL = FNEW(None, 32)

# Positions
PLTOP = 0
PLCENTER = 1
PLBOTTOM = 2
PCTOP = 3
PCCENTER = 4
PCBOTTOM = 5
PRTOP = 6
PRCENTER = 7
PRBOTTOM = 8
PFILL = 9

# Stacks. Don't use unless you know what you're doing
PSTACKS = {
    PLTOP:    ([1, 0],  lambda size, sizeofobj: (0, 0)),
    PLCENTER: ([1, 0],  lambda size, sizeofobj: (0, round(size[1]/2-sizeofobj[1]/2))),
    PLBOTTOM: ([1, 0],  lambda size, sizeofobj: (0, size[1]-sizeofobj[1])),
    PCTOP:    ([0, 1],  lambda size, sizeofobj: (round(size[0]/2-sizeofobj[0]/2), 0)),
    PCCENTER: ([0, 1],  lambda size, sizeofobj: (round(size[0]/2-sizeofobj[0]/2), round(size[1]/2-sizeofobj[1]/2))),
    PCBOTTOM: ([0, -1], lambda size, sizeofobj: (round(size[0]/2-sizeofobj[0]/2), size[1]-sizeofobj[1])),
    PRTOP:    ([-1, 0], lambda size, sizeofobj: (size[0]-sizeofobj[0], 0)),
    PRCENTER: ([-1, 0], lambda size, sizeofobj: (size[0]-sizeofobj[0], round(size[1]/2-sizeofobj[1]/2))),
    PRBOTTOM: ([-1, 0], lambda size, sizeofobj: (size[0]-sizeofobj[0], size[1]-sizeofobj[1])),
    PFILL:    ([0, 0],  lambda size, sizeofobj: (0, 0))
}

PIDX = 0 # DO NOT USE UNLESS YOU REALLY KNOW WHAT YOU'RE DOING

def PNEW(stack, func, idx=None): # To create new layouts
    global PIDX
    if idx == None:
        idx = PIDX
        PIDX += 1
    PSTACKS[idx+10] = (stack, func)
    return idx+10

def PSTATIC(x, y, idx=None): # To put an element at a specific x and y location
    global PIDX
    if idx == None:
        idx = PIDX
        PIDX += 1
    PSTACKS[idx+10] = ([0, 0], lambda _, __: (x, y))
    return idx+10

# Events
EFIRST = 0
ELOADUI = 1
ETICK = 2
EELEMENTCLICK = 3
EEVENT = 4
ELAST = 5

# Types
TBUTTON = 0
TTEXTBOX = 1
TINPUTBOX = 2
TSWITCH = 3

# Resizes
RWIDTH = 0
RHEIGHT = 1
RNONE = 2
