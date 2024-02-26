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

# font Sides
# Weighting
SWLEFT = 0
SWTOP = 0
SWMID = 0.5
SWBOT = 1
SWRIGHT = 1
# Direction
SDLEFTRIGHT = 3
SDUPDOWN = 4

# Fonts
class FNEW:
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
        dir : GO.SD______, optional
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
                sur.blit(i.convert_alpha(), (pos, (sze[1]-i.get_height())*weight))
                pos += i.get_width()
            else:
                sur.blit(i.convert_alpha(), ((sze[0]-i.get_width())*weight, pos))
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
