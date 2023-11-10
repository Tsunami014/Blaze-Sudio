import pygame

# Colours
CWHITE = (255, 255, 255)
CGREEN = (10, 255, 50)
CRED = (255, 10, 50)
CBLUE = (10, 50, 255)
CBLACK = (0, 0, 0)
CYELLOW = (255, 200, 50)
CGREY = (125, 125, 125)

# Fonts
FTITLE = pygame.font.SysFont('Comic Sans MS', 64, True)
FCODEFONT = pygame.font.SysFont('Lucida Sans Typewriter', 16)
FFONT = pygame.font.SysFont(None, 52)

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
    if idx == None:
        idx = PIDX
        PIDX += 1
    PSTACKS[idx+10] = (stack, func)
    return idx+10

# Events
TFIRST = 0
TLOADUI = 1
TTICK = 2
TELEMENTCLICK = 3
TLAST = 4
