from dataclasses import dataclass, field
import pygame
import pygame.freetype
from string import printable

# TODO: Modify the __str__ and __repr__ of the class to a name
def Base(cls=None, default=True):
    def wrap(clss):
        return dataclass(clss, unsafe_hash=True, init=default, repr=default)
    if cls is None:
        # @Base()
        return wrap
    # @Base
    return wrap(cls)

# Colours
@Base(default=False)
class C___(tuple):
    def __init__(self, colourtuple, name='C___'):
        self.name = name
    def __str__(self):
        return f'<C{self.name} col=({str(list(self))[1:-1]})>'
    def __repr__(self): return str(self)
CTRANSPARENT = C___((255, 255, 255, 1), name='TRANSPARENT')
CWHITE =  C___((255, 255, 255), name='WHITE')
CAWHITE = C___((200, 200, 200), name='ALMOSTWHITE')
CGREEN =  C___((60, 200, 100),  name='GREEN')
CRED =    C___((255, 60, 100),  name='RED')
CBLUE =   C___((60, 100, 255),  name='BLUE')
CBLACK =  C___((0, 0, 0),       name='BLACK')
CYELLOW = C___((255, 200, 50),  name='YELLOW')
CGREY =   C___((125, 125, 125), name='GREY')
def CNEW(name):
    c = pygame.color.Color(name)
    return C___((c.r, c.g, c.b), name=name)
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

# font Sides
# Weighting
@Base
class SW__:
    w: int
SWLEFT =  SW__(0)
SWTOP =   SW__(0)
SWMID =   SW__(0.5)
SWBOT =   SW__(1)
SWRIGHT = SW__(1)
# Direction
@Base
class SD__:
    idx: int
SDLEFTRIGHT = SD__(0)
SDUPDOWN =    SD__(1)

# Fonts
class F___:
    def __init__(self, name, size, bold=False, italic=False):
        self.font = pygame.font.SysFont(name, size, bold, italic)
        self.emojifont = pygame.freetype.SysFont('segoeuisymbol', size, bold, italic)
    def render(self, txt, col, updownweight=SWMID, leftrightweight=SWMID, allowed_width=None, renderdash=True):
        """
        Renders some text with emoji support!

        Parameters
        ----------
        txt : str
            The text to render!
        col : tuple[int,int,int]
            The colour of the text
        updownweight : GO.SW___, optional
            The weight of the text up-down; make the text weighted towards the top, middle, or bottom, by default SWMID
            You probably do not want to change this
        leftrightweight : GO.SW___, optional
            The weight of the text left-right, by default SWMID
            This only ever comes into effect if allowed_width is not None and there is enough text to span multiple lines
            You probably want to change this occasionally
        allowed_width : int, optional
            The allowed width of the text, by default None
            If the text goes over this amount of pixels, it makes a new line
            None disables it
        renderdash : bool, optional
            Whether or not to render the '-' at the end of lines of text that are too big to fit on screen, by default True

        Returns
        -------
        pygame.Surface
            The surface of the text!
        """
        if txt == '':
            return pygame.Surface((0, 0))
        if allowed_width is None:
            return self.combine(self.split(txt, col), weight=updownweight)
        else:
            # Thanks to https://stackoverflow.com/questions/49432109/how-to-wrap-text-in-pygame-using-pygame-font-font for the font wrapping thing
            # Split text into words
            words = txt.split(' ')
            # now, construct lines out of these words
            lines = []
            while len(words) > 0:
                # get as many words as will fit within allowed_width
                line_words = []
                while len(words) > 0:
                    line_words.append(words.pop(0))
                    fw, fh = self.size(' '.join(line_words + words[:1]))
                    if fw > allowed_width:
                        break
                # add a line consisting of those words
                line = ' '.join(line_words)
                if len(line_words) == 1 and self.size(line_words[0])[0] > allowed_width:
                    out = []
                    line = ''
                    for i in line_words[0]:
                        if renderdash:
                            fw, fh = self.size(line+'--')
                            if fw > allowed_width:
                                out.append(line+'-')
                                line = i
                            else:
                                line += i
                        else:
                            fw, fh = self.size(line+'-')
                            if fw > allowed_width:
                                out.append(line)
                                line = i
                            else:
                                line += i
                    #if line != '': out.append(line)
                    lines.extend(out)
                lines.append(line)
            return self.combine([self.combine(self.split(i, col), updownweight) for i in lines], leftrightweight, SDUPDOWN)
    
    def split(self, txt, col):
        """
        Splits text and renders it!
        This splits text up into 2 different parts:
        The part with regular renderable text and the part without (i.e. emojis, other stuff)
        It then uses the 2 different fonts, one for rendering text and the other for non-text
        And renders them all seperately and then makes a list of the outputs!

        Parameters
        ----------
        txt : str
            The text to split
        col : tuple[int,int,int]
            The colour of the text

        Returns
        -------
        list[pygame.Surface]
            A list of pygame surfaces of all the different texts rendered!
            You can use `FNEW.combine(surs)` to combine the surfaces!
        """
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
        return parts
    
    def combine(self, surs, weight=SWMID, dir=SDLEFTRIGHT):
        """
        Combines multiple surfaces into one!

        Parameters
        ----------
        surs : list[pygame.Surface]
            The list of surfaces to combine!
        weight : GO.SW___, optional
            The weight of the combine, i.e. make al the text from left to right, centred, etc., by default SWMID
        dir : GO.SD___, optional
            The direction of the combine; i.e. combine all the texts into one long text or make them all have new lines, by default SDLEFTRIGHT

        Returns
        -------
        pygame.Surface
            The combined surface!
        """
        if dir == SDLEFTRIGHT:
            sze = (sum([i.get_width() for i in surs]), max([i.get_height() for i in surs]))
        else:
            sze = (max([i.get_width() for i in surs]), sum([i.get_height() for i in surs]))
        sur = pygame.Surface(sze).convert_alpha()
        sur.fill((255, 255, 255, 1))
        pos = 0
        for i in surs:
            if dir == SDLEFTRIGHT:
                sur.blit(i.convert_alpha(), (pos, (sze[1]-i.get_height())*weight.w))
                pos += i.get_width()
            else:
                sur.blit(i.convert_alpha(), ((sze[0]-i.get_width())*weight.w, pos))
                pos += i.get_height()
        return sur  
    
    def size(self, txt):
        """
        Gets the size of the font if you render a certain text!

        Parameters
        ----------
        txt : str
            The text to render and see the size of

        Returns
        -------
        tuple[int,int]
            The size of the output font
        """
        surs = self.split(txt, (0, 0, 0))
        return (sum([i.get_width() for i in surs]), max([i.get_height() for i in surs]))

class FNEW(F___): pass # Making new fonts

FTITLE =    F___('Comic Sans MS', 64, True)
FCODEFONT = F___('Lucida Sans Typewriter', 16)
FFONT =     F___(None, 52)
FSMALL =    F___(None, 32)

# Positions
@Base
class P___:
    idx: int
    lmr: int | None # Left(0) Middle(1) Right(2)
    umd: int | None # Up(0) Middle(1) Down(2)

PLTOP =    P___(0, 0, 0)
PLCENTER = P___(1, 0, 1)
PLBOTTOM = P___(2, 0, 2)
PCTOP =    P___(3, 1, 0)
PCCENTER = P___(4, 1, 1)
PCBOTTOM = P___(5, 1, 2)
PRTOP =    P___(6, 2, 0)
PRCENTER = P___(7, 2, 1)
PRBOTTOM = P___(8, 2, 2)
PFILL =    P___(9, None, None)

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

def PNEW(stack, func, idx=None, lmr=None, umd=None): # To create new layouts
    global PIDX
    if idx == None:
        idx = PIDX
        PIDX += 1
    pos = P___(idx+10, lmr, umd)
    PSTACKS[pos] = (stack, func)
    return pos

def PSTATIC(x, y, idx=None): # To put an element at a specific x and y location
    global PIDX
    if idx == None:
        idx = PIDX
        PIDX += 1
    pos = P___(idx+10, None, None)
    PSTACKS[pos] = ([0, 0], lambda _, __: (x, y))
    return pos

# Events
@Base
class E___:
    idx: int
    doc: str
    passed: dict = field(default_factory=dict)

EFIRST =        E___(0, 'The first event, before the screen has even displayed it\'s first frame')
ELOADUI =       E___(1, 'Every time it loads the UI (first, when G.Refresh, etc.) it calls this function.')
ETICK =         E___(2, 'Each tick this is ran')
EELEMENTCLICK = E___(3, 'When an element is clicked, this is ran', {'element': 'The element that got clicked'})
EEVENT =        E___(4, 'When a pygame event occurs (click mouse, press button, etc.)', {'element': 'The pygame.event.Event that occured'})
ELAST =         E___(5, 'Just before quitting this is ran', {'aborted': 'Whether or not the graphic screen was aborted due to G.Abort()'})

# Types
@Base
class T___:
    idx: int
TBUTTON =   T___(0)
TTEXTBOX =  T___(1)
TINPUTBOX = T___(2)
TSWITCH =   T___(3)

# Resizes
@Base
class R___:
    idx: int
RWIDTH =  R___(0)
RHEIGHT = R___(1)
RNONE =   R___(2)
