import pygame

# Colours
CTRANSPARENT = (255, 255, 255, 1)
CWHITE = (255, 255, 255)
CGREEN = (10, 255, 50)
CRED = (255, 10, 50)
CBLUE = (10, 50, 255)
CBLACK = (0, 0, 0)
CYELLOW = (255, 200, 50)
CGREY = (125, 125, 125)
def CNEW(name):
    c = pygame.color.Color(name)
    return (c.r, c.g, c.b)
CINACTIVE = CNEW('lightskyblue3')
CACTIVE = CNEW('dodgerblue2')

# Fonts
FTITLE = pygame.font.SysFont('Comic Sans MS', 64, True)
FCODEFONT = pygame.font.SysFont('Lucida Sans Typewriter', 16)
FFONT = pygame.font.SysFont(None, 52)
FSMALL = pygame.font.SysFont(None, 32)

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
