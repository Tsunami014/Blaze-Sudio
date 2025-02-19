from dataclasses import dataclass
import pygame
import pygame.freetype
from string import printable

# TODO: Make these all enums

# TODO: Modify the __str__ and __repr__ of the class to a name
def Base(cls=None, default=True, str=True, addhash=True):
    def wrap(clss):
        return dataclass(clss, unsafe_hash=addhash, init=default, repr=default and str)
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
CMAUVE =  C___((173, 127, 168), name='MAUVE')
CPURPLE = C___((92, 53, 102),   name='PURPLE')
def CNEW(name):
    c = pygame.color.Color(name)
    return C___((c.r, c.g, c.b), name=name)
CORANGE = CNEW('orange')
CINACTIVE = CNEW('lightskyblue3')
CACTIVE = CNEW('dodgerblue2')

CRAINBOWCOLOURS = [
    CRED,
    CORANGE,
    CYELLOW,
    CGREEN,
    CBLUE,
    CNEW('magenta'),
    CMAUVE,
    CGREY
]

def CRAINBOW():
    while True:
        for i in CRAINBOWCOLOURS:
            yield i

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
FERRORED = False
class F___:
    def __init__(self, name, size, bold=False, italic=False):
        self.font = pygame.font.SysFont(name, size, bold, italic)
        fonts = pygame.sysfont.get_fonts()
        emojis = [font for font in fonts if "emoji" in font]
        if len(emojis) == 0:
            global FERRORED
            if not FERRORED:
                print("Unable to find a font that supports emojis for your system! Using regular fonts instead.")
                FERRORED = True
            self.emojifont = self.font
        else:
            self.emojifont = pygame.font.SysFont(emojis[0], size, bold, italic)
    
    def render(self, 
               txt: str, 
               col: C___, 
               updownweight: SW__ = SWMID, 
               leftrightweight: SW__ = SWMID, 
               allowed_width: int = None, 
               renderdash: bool = True, 
               verbose: bool = False
        ):
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
        verbose : bool, optional
            Returns extra information, by default False

        Returns
        -------
        If not verbose:
            pygame.Surface
                The surface of the text!
        Else:
            pygame.Surface
                The surface of the text!
            int
                The amount of lines rendered
        """
        if isinstance(txt, pygame.Surface):
            return txt
        
        txt = txt.replace('\t', '    ')
        if txt == '':
            if verbose:
                return pygame.Surface((0, 0)), 0
            return pygame.Surface((0, 0))
        if allowed_width is None:
            lines = txt.split('\n')
            combined_lines = [self.combine(self.split(line, col), weight=updownweight) for line in lines if line != '']
            combined = self.combine(combined_lines, weight=leftrightweight, dir=SDUPDOWN)
            if verbose:
                return combined, len(lines)
            return combined
        else:
            masterlines = []
            for ln in txt.split('\n'):
                # Thanks to https://stackoverflow.com/questions/49432109/how-to-wrap-text-in-pygame-using-pygame-font-font for the font wrapping thing
                # Split text into words
                words = ln.split(' ')
                # now, construct lines out of these words
                lines = []
                while len(words) > 0:
                    # get as many words as will fit within allowed_width
                    line_words = []
                    while len(words) > 0:
                        line_words.append(words.pop(0))
                        fw, fh = self.winSze(' '.join(line_words + words[:1]))
                        if fw > allowed_width:
                            break
                    # add a line consisting of those words
                    line = ' '.join(line_words)
                    if len(line_words) == 1 and self.winSze(line_words[0])[0] > allowed_width:
                        out = []
                        line = ''
                        for i in line_words[0]:
                            if renderdash:
                                fw, fh = self.winSze(line+'--')
                                if fw > allowed_width:
                                    out.append(line+'-')
                                    line = i
                                else:
                                    line += i
                            else:
                                fw, fh = self.winSze(line+'-')
                                if fw > allowed_width:
                                    out.append(line)
                                    line = i
                                else:
                                    line += i
                        #if line != '': out.append(line)
                        lines.extend(out)
                    lines.append(line)
                masterlines.extend(lines)
            combined = self.combine([self.combine(self.split(i, col), updownweight) for i in masterlines if i != ''], leftrightweight, SDUPDOWN)
            if verbose:
                return combined, len(masterlines)
            return combined
    
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
                    parts.append(pygame.transform.scale(self.emojifont.render(part, 1, col), (self.font.get_linesize(), self.font.get_linesize())))
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
        sur = pygame.Surface(sze, pygame.SRCALPHA)
        sur.fill((255, 255, 255, 0))
        pos = 0
        for i in surs:
            if dir == SDLEFTRIGHT:
                sur.blit(i, (pos, (sze[1]-i.get_height())*weight.w))
                pos += i.get_width()
            else:
                sur.blit(i, ((sze[0]-i.get_width())*weight.w, pos))
                pos += i.get_height()
        return sur
    
    @property
    def linesize(self):
        return self.font.get_linesize() # max(self.font.get_linesize(), self.emojifont.get_linesize())
    
    def winSze(self, txt):
        """
        Gets the winSze of the font if you render a certain text!

        Parameters
        ----------
        txt : str
            The text to render and see the winSze of

        Returns
        -------
        tuple[int,int]
            The winSze of the output font
        """
        if txt == '':
            return (0, 0)
        surs = self.split(txt, (0, 0, 0))
        return (sum([i.get_width() for i in surs]), max([i.get_height() for i in surs]))

class FNEW(F___):
    pass # Making new fonts

def findAFont(*fontOpts):
    """
    Finds the first avaliable font on the user's machine.

    Returns:
        str | None: The first string in the options list provided that is on the user's machine, on None if none of them are avaliable.
    """
    fs = pygame.font.get_fonts()
    for font in fontOpts:
        if font in fs:
            return font
    return None

FTITLE =       F___(findAFont('conicsansms', 'dejavuserif'), 64, True)
FCODEFONT =    F___(findAFont('lucidasanstypewriterregular', 'ubuntusansmono'), 16)
FCODEREGULAR = F___(findAFont('lucidasanstypewriterregular', 'ubuntusansmono'), 52)
FFONT =        F___(None, 52)
FSMALL =       F___(None, 32)

# Positions
class POverride:
    """The base class for position overrides. Do not use directly."""
    winSze = None
    """Set in some cases, so it is kept here so nothing goes wrong, but never used."""
    def setup(self, element, Graphic):
        self.elm = element
        self.G = Graphic
    
    def copy(self):
        return POverride()
    
    def remove(self):
        pass
    
    def __call__(self):
        return 0, 0

@Base(addhash=False)
class P___:
    weighting: tuple[int,int]
    """
- 0 = left/top of screen
- 1 = right/bottom of screen
- any other decimal between is that much through the screen
    """
    stack: tuple[int,int]
    """
Which direction new elements will be placed. 1 = going right/down, -1 = going left/up, 0 = not going anywhere in that direction.
    """
    centre: tuple[bool,bool]
    
    def __call__(self, winSze, objSze, allSizes, idx):
        if self.weighting[0] == 0:
            xoff = 0
        elif self.weighting[0] == 1:
            xoff = objSze[0]
        else:
            xoff = objSze[0]/2
        if self.centre[0]:
            if self.stack[0] != 0:
                xoff = abs(sum(i[0]*self.stack[0] for i in allSizes))/2
        outx = winSze[0]*self.weighting[0]-xoff + sum(i[0]*self.stack[0] for i in allSizes[:idx])

        if self.weighting[1] == 0:
            yoff = 0
        elif self.weighting[1] == 1:
            yoff = objSze[1]
        else:
            yoff = objSze[1]/2
        if self.centre[1]:
            if self.stack[1] != 0:
                yoff = abs(sum(i[1]*self.stack[1] for i in allSizes))/2
        outy = winSze[1]*self.weighting[1]-yoff + sum(i[1]*self.stack[1] for i in allSizes[:idx])
        return (round(outx), round(outy))

    def copy(self):
        return PNEW(self.weighting, self.stack, self.centre)
    
    def __hash__(self):
        return hash((id(self), self.weighting, self.stack, self.centre))

PLTOP =    P___((0, 0), (0, 1), (False, False))
PLCENTER = P___((0, 0.5), (0, 1), (False, True))
PLBOTTOM = P___((0, 1), (1, 0), (False, False))
PCTOP =    P___((0.5, 0), (0, 1), (True, False))
PCCENTER = P___((0.5, 0.5), (0, 1), (True, True))
PCBOTTOM = P___((0.5, 1), (0, -1), (True, False))
PRTOP =    P___((1, 0), (0, 1), (False, False))
PRCENTER = P___((1, 0.5), (0, 1), (False, True))
PRBOTTOM = P___((1, 1), (-1, 0), (False, False))

def PNEW(weighting, stack, centre=(False, False)): # To create new layouts
    if isinstance(weighting, P___):
        weighting = weighting.weighting
    if isinstance(stack, P___):
        stack = stack.stack
    if isinstance(centre, P___):
        centre = centre.centre
    
    return P___(weighting, stack, centre)

class PSTATIC(POverride):
    def __init__(self, x, y):
        self.pos = (x, y)
    
    def copy(self):
        return PSTATIC(*self.pos)
    
    def __call__(self):
        return self.pos

# Types
@Base(str=False)
class T___:
    def __str__(self):
        return f'<T{self.name}>'
    def __repr__(self): return str(self)
    idx: int
    name: str
TBUTTON =     T___(0,  'Button'    )
TINPUTBOX =   T___(1,  'Inputbox'  )
TNUMBOX =     T___(2,  'Numbox'    )
TTEXTBOX =    T___(3,  'Textbox'   )
TSWITCH =     T___(4,  'Switch'    )
TCHECKBOX =   T___(5,  'Checkbox'  )
TFRAME =      T___(6,  'Frame'     )
TLAYOUT =     T___(7,  'Layout'    )
TSTATIC =     T___(8,  'Static'    )
TCOLOURPICK = T___(9,  'ColourPick')
TTOAST =      T___(10,  'Toast'    )
TEMPTY =      T___(11, 'Empty'     )


# Resizes
@Base
class R___:
    idx: int
RWIDTH =  R___(0)
RHEIGHT = R___(1)
RNONE =   R___(2)
