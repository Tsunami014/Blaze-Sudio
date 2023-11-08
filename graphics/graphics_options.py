import pygame

# Colours
CWHITE = (255, 255, 255)
CGREEN = (10, 255, 50)
CRED = (255, 10, 50)
CBLUE = (10, 50, 255)
CBLACK = (0, 0, 0)

# Fonts
FTITLE = pygame.font.SysFont('Comic Sans MS', 64, True)
FCODEFONT = pygame.font.SysFont('Lucida Sans Typewriter', 16)
FFONT = pygame.font.SysFont(None, 52)

# Positions
PCENTER = lambda size, sizeofobj: (round(size[0]/2-sizeofobj[0]/2), round(size[1]/2-sizeofobj[1]/2))
PTOPCENTER = lambda size, sizeofobj: (round(size[0]/2-sizeofobj[0]/2), 0)
PBOTTOMCENTER = lambda size, sizeofobj: (round(size[0]/2-sizeofobj[0]/2), size[1]-sizeofobj[1])
