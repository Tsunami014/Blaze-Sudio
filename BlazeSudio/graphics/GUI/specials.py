from typing import Iterable
import pygame
from BlazeSudio.graphics import mouse, options as GO
from BlazeSudio.graphics.GUI.base import Element, ReturnState
from BlazeSudio.graphics.stacks import Stack
from BlazeSudio.graphics.stuff import Collection

__all__ = [
    'TerminalBar',
    'ScrollableFrame',
    'ScaledFrame',
    'BaseFrame',
    'GraphicBase'
]

class GraphicBase:
    """This contains all the things an object needs to be a graphic object and is not meant to be used directly."""
    # Stuff that needs replacing with instance (not class) variables (but have been provided as instants for convenience):
    WIN: pygame.Surface = pygame.Surface((0, 0))
    size: tuple[int, int] = (0, 0)
    stacks: Stack = Stack()
    Stuff: Collection = Collection()
    pause: bool = False

    # Functions that need replacing:
    def Abort(self):
        pass

    # Things that don't need replacing:
    def _updateStuff(self, mousepos, evnts):
        calls = []
        returns = self.Stuff.update(mousepos, evnts.copy())
        for obj in returns:
            retValue = returns[obj]
            if retValue is None:
                continue

            if isinstance(retValue, list):
                calls.extend(retValue)
                continue
            
            for ret in retValue.get():
                if ret == ReturnState.ABORT:
                    self.Abort()
                elif ret == ReturnState.CALL:
                    calls.append(obj)
                elif ret == ReturnState.REDRAW:
                    obj.update(mousepos, evnts.copy(), True) # Redraw forcefully on top of everything else
        return calls
    
    def getAllElms(self):
        return self.Stuff.getall()
    
    def __getitem__(self, key):
        return self.Stuff[key]
    
    def __setitem__(self, key, value):
        self.Stuff[key] = value
    
    @property
    def layers(self):
        return self.Stuff.layers

class BaseFrame(GraphicBase, Element):
    type = GO.TSCROLLABLE
    def __init__(self, 
                 G, 
                 pos: GO.P___, 
                 size: Iterable[int], 
                 outline: int = 10, 
                 outlinecol: GO.C___ = GO.CGREY, 
                 bgcol: GO.C___ = GO.CWHITE
                ):
        """
        The base Frame object from which many other Frames are made from.

        Args:
            G (Graphic): The Graphic object to add this to.
            pos (GO.P___): The position of this object in the Graphic screen.
            size (Iterable[int]): The size of the screen
            outline (int, optional): The thickness of the outline of the element. Defaults to 10.
            outlinecol (GO.C___, optional): The colour of the outline. Defaults to GO.CGREY.
            bgcol (GO.C___, optional): The background colour to the new Graphic-like object. Defaults to GO.CWHITE.
        """
        super().__init__(G, pos, size)
        self.WIN = pygame.Surface(size)
        self.bgcol = bgcol
        self.outline = (outline, outlinecol)
        self.stacks = Stack()
        self.Stuff = Collection()
    
    @property
    def pause(self):
        return self.G.pause
    
    @pause.setter
    def pause(self, newpause):
        self.G.pause = newpause
    
    @property
    def sizeOfScreen(self):
        return self.WIN.get_size()
    
    @sizeOfScreen.setter
    def sizeOfScreen(self, newSze):
        if newSze == self.sizeOfScreen:
            return
        self.WIN = pygame.Surface(newSze)
        for elm in self.getAllElms():
            elm.stackP.winSze = newSze
    
    def get(self):
        """Get all the stuff in the frame"""
        return self.Stuff
    
    def update(self, mousePos, events):
        x, y = self.stackP()
        self.WIN.fill(self.bgcol)
        if pygame.Rect(x, y, *self.size).collidepoint(mousePos):
            mp = (mousePos[0]-x, mousePos[1]-y)
        else:
            mp = (float('inf'), float('inf'))
        
        calls = self._updateStuff(mp, events)
        self.G.WIN.blit(self.WIN, (x, y))
        if self.outline[0] != 0:
            pygame.draw.rect(self.G.WIN, self.outline[1], pygame.Rect(x, y, *self.size), self.outline[0], 3)
        
        return calls
    
    def Abort(self):
        self.G.Abort()

class ScrollableFrame(BaseFrame):
    def __init__(self, 
                 G, 
                 pos: GO.P___, 
                 goalrect: Iterable[int], 
                 sizeOfScreen: Iterable[int], 
                 outline: int = 10, 
                 bar: bool = True, 
                 outlinecol: GO.C___ = GO.CGREY, 
                 bgcol: GO.C___ = GO.CWHITE
                ):
        """
        A scrollable object which is just like a Graphic but can be scrolled through and used as an Element in existing Graphics.

        Args:
            G (Graphic): The Graphic object to add this to.
            pos (GO.P___): The position of this object in the Graphic screen.
            goalrect (Iterable[int]): The size of *this* object in the *existing* Graphic screen.
            sizeOfScreen (Iterable[int]): The size of the *new* Graphic screen.
            outline (int, optional): The thickness of the outline of the element. Defaults to 10.
            bar (bool, optional): Whether or not to have a scrollbar down the side. Defaults to True.
            outlinecol (GO.C___, optional): The colour of the outline. Defaults to GO.CGREY.
            bgcol (GO.C___, optional): The background colour to the new Graphic-like object. Defaults to GO.CWHITE.
        """
        super().__init__(G, pos, goalrect, outline, outlinecol, bgcol)
        self.WIN = pygame.Surface(sizeOfScreen)
        self.bar = bar
        self.scroll = 0
    
    def get(self):
        """Get the scroll value"""
        return self.scroll
    
    def set(self, scroll):
        """Set the scroll value"""
        self.scroll = scroll
    
    def update(self, mousePos, events):
        mouseColliding = pygame.Rect(*self.stackP(), *self.size).collidepoint(mousePos)
        if mouseColliding and not self.G.pause:
            for ev in events:
                if ev.type == pygame.MOUSEWHEEL:
                    y = ev.y - 1
                    if 0 <= y <= 1:
                        y = 2
                    self.scroll += y * 2
                    self.scroll = min(max(-self.sizeOfScreen[1]+self.size[1], self.scroll), 0)
        x, y = self.stackP()
        self.WIN.fill(self.bgcol)
        if mouseColliding:
            mp = (mousePos[0]-x, mousePos[1]-y-self.scroll)
        else:
            mp = (float('inf'), float('inf'))
        calls = self._updateStuff(mp, events)
        self.G.WIN.blit(self.WIN, (x, y), pygame.Rect(0, -self.scroll, *self.size))
        if self.outline[0] != 0:
            pygame.draw.rect(self.G.WIN, self.outline[1], pygame.Rect(x, y, *self.size), self.outline[0], 3)
        if self.bar:
            try:
                try:
                    w = self.outline[0]/2
                except ZeroDivisionError:
                    w = 0
                p = (x+self.size[0]-w, y+((-self.scroll) / (self.sizeOfScreen[1]-self.size[1]))*(self.size[1]-40)+20)
                pygame.draw.line(self.G.WIN, (200, 50, 50), (p[0], p[1]-20), (p[0], p[1]+20), 10)
            except:
                pass
        return calls

class ScaledFrame(BaseFrame):
    def __init__(self, 
                 G, 
                 pos: GO.P___, 
                 size: Iterable[int], 
                 scale: int = 2,
                 outline: int = 10, 
                 outlinecol: GO.C___ = GO.CGREY, 
                 bgcol: GO.C___ = GO.CWHITE
                ):
        """
        The base Frame object from which many other Frames are made from.

        Args:
            G (Graphic): The Graphic object to add this to.
            pos (GO.P___): The position of this object in the Graphic screen.
            size (Iterable[int]): The size of the screen.
            scale (int, optional): The scale of the screen. Defaults to 2.
            outline (int, optional): The thickness of the outline of the element. Defaults to 10.
            outlinecol (GO.C___, optional): The colour of the outline. Defaults to GO.CGREY.
            bgcol (GO.C___, optional): The background colour to the new Graphic-like object. Defaults to GO.CWHITE.
        """
        super().__init__(G, pos, size, outline, outlinecol, bgcol)
        self._scale = None
        self.scale = scale
    
    @property
    def sizeOfScreen(self):
        return self.WIN.get_size()
    
    @property
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, newSze):
        if newSze == self._scale:
            return
        if newSze <= 0:
            raise ValueError("Scale cannot be less than or equal to 0")
        self._scale = newSze
        self.WIN = pygame.Surface((self.size[0]/self._scale, self.size[1]/self._scale))
        for elm in self.getAllElms():
            elm.stackP.winSze = self.sizeOfScreen
    
    def update(self, mousePos, events):
        x, y = self.stackP()
        self.WIN.fill(self.bgcol)
        if pygame.Rect(x, y, *self.size).collidepoint(mousePos):
            mp = ((mousePos[0]-x)/self._scale, (mousePos[1]-y)/self._scale)
        else:
            mp = (float('inf'), float('inf'))
        calls = self._updateStuff(mp, events)
        self.G.WIN.blit(pygame.transform.scale(self.WIN, self.size), (x, y))
        if self.outline[0] != 0:
            pygame.draw.rect(self.G.WIN, self.outline[1], pygame.Rect(x, y, *self.size), self.outline[0], 3)
        return calls

class TerminalBar(Element):
    def __init__(self, G, spacing=5):
        """
        Adds a terminal bar to the bottom of your screen! You can use this for debugging and can run commands using it also for debugging!
        Or just have it as a feature in your game!

        Args:
            G (Graphic): The graphic screen to attach to
            spacing (int, optional): The spacing between the text and the top and bottom of the bar. Defaults to 5.
        """
        self.G = G
        self.spacing = spacing
        r = GO.FCODEFONT.render('> ', GO.CWHITE)
        h = r.get_height()+self.spacing*2
        super().__init__(G, (0, self.G.WIN.get_height()-h), (self.G.WIN.get_width(), h))
        self.active = -1
        self.txt = ''
        self._onEnters = []
    
    def onEnter(self, func):
        self._onEnters.append(func)
        return func
    
    def pressed(self, event):
        if event.key == pygame.K_RETURN:
            txt = self.txt
            self.txt = ""
            for f in self._onEnters:
                f(txt)
            self.active = -1
        elif event.key == pygame.K_BACKSPACE:
            self.txt = self.txt[:-1]
        else:
            self.txt += event.unicode
    
    def toggleactive(self, forceactive=None):
        if forceactive is not None:
            if forceactive:
                self.active = 60
            else:
                self.active = -1
        if self.active == -1:
            self.active = 60
        else:
            self.active = -1
    
    def update(self, mousePos, events):
        if not self.G.pause:
            if self.collides(*mousePos):
                mouse.Mouse.set(mouse.MouseState.TEXT)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F5:
                        self.toggleactive()
                        if self.txt == "" and self.active != -1:
                            self.txt = "/"
                    elif self.active != -1:
                        self.pressed(event)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and not self.G.pause:
                    if event.button == pygame.BUTTON_LEFT:
                        self.toggleactive(not self.collides(*mousePos))
        
        if self.active >= 0:
            self.active -= 1
            if self.active <= 0:
                self.active = 60
        r = self.render()
        h = r.get_height()+self.spacing*2
        pygame.draw.rect(self.G.WIN, GO.CBLACK, pygame.Rect(0, self.G.WIN.get_height()-h, self.G.WIN.get_width(), h))
        self.G.WIN.blit(r, (self.spacing, self.G.WIN.get_height()-h+self.spacing))
    
    @property
    def height(self):
        return self.render().get_height()+self.spacing*2

    def render(self):
        t = '> '+self.txt
        if self.active >= 30:
            t += '_'
        r = GO.FCODEFONT.render(t, GO.CWHITE)
        return r
    
    def collides(self, x, y):
        h = self.height
        return pygame.Rect(0, self.G.WIN.get_height()-h, self.G.WIN.get_width(), h).collidepoint(x, y)
    

    def get(self):
        return self.txt
    
    def set(self, txt):
        self.txt = txt
    
    def __str__(self):
        return '<TerminalBar>'
    def __repr__(self): return str(self)
