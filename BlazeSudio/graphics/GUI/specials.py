from typing import Iterable
import pygame
from time import time
from BlazeSudio.graphics import mouse, options as GO
from BlazeSudio.graphics.GUI.base import Element, ReturnState
from BlazeSudio.graphics.stacks import Stack
from BlazeSudio.graphics.stuff import Collection

__all__ = [
    'TerminalBar',
    'ScrollableFrame',
    'ScaledByFrame',
    'PopupFrame',
    'GridLayout',

    'PresetFrame',

    'BaseFrame',
    'BaseLayout',
    'GraphicBase',

    'LayoutPos',
    'Infinity'
]

class Infinity(float):
    def __new__(cls, real):
        instance = super().__new__(cls, 'inf')
        instance.val = real
        return instance

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
        oldMP = mousepos
        for i in self.Stuff:
            if isinstance(i, GraphicBase) and pygame.Rect(*i.stackP(), *i.size).collidepoint(mousepos):
                mousepos = (Infinity(mousepos[0]), Infinity(mousepos[1]))
                break
        calls = []
        redraw_tops = []
        redraw_vtops = []
        # TODO: Have return states able to be passed down instead of just the calls
        def handle_returns(returns, care4Redraw=False):
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
                    elif care4Redraw:
                        if ret == ReturnState.REDRAW:
                            obj.update(mousepos, evnts.copy(), True) # Redraw forcefully on top of everything else
                        elif ret == ReturnState.REDRAW_HIGH:
                            redraw_tops.append(obj)
                        elif ret == ReturnState.REDRAW_HIGHEST:
                            redraw_vtops.append(obj)
        handle_returns(self.Stuff.update(mousepos, evnts.copy()), True)
        moreRets = {}
        for obj in redraw_tops:
            moreRets[obj] = obj.update(oldMP, evnts.copy(), True) # Redraw on top of everything
        for obj in redraw_vtops:
            moreRets[obj] = obj.update(oldMP, evnts.copy(), True) # Redraw on top of LITERALLY everything
        handle_returns(moreRets)
        return calls
    
    def get(self):
        return self.Stuff.getall()
    
    def __getitem__(self, key):
        return self.Stuff[key]
    
    def __setitem__(self, key, value):
        self.Stuff[key] = value
    
    @property
    def layers(self):
        return self.Stuff.layers

class BaseFrame(GraphicBase, Element):
    type = GO.TFRAME
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
        for elm in self.get():
            elm.stackP.winSze = newSze
    
    def update(self, mousePos, events, force_redraw=False):
        if force_redraw:
            return self._update(mousePos, events)
        else:
            return ReturnState.REDRAW_HIGH
    
    def _update(self, mousePos, events):
        x, y = self.stackP()
        self.WIN.fill(self.bgcol)
        if pygame.Rect(x, y, *self.size).collidepoint(mousePos):
            mp = (mousePos[0]-x, mousePos[1]-y)
            mouse.Mouse.set(mouse.MouseState.NORMAL)
        else:
            mp = (Infinity(mousePos[0]-x), Infinity(mousePos[1]-y))
        
        calls = self._updateStuff(mp, events)
        self.G.WIN.blit(self.WIN, (x, y))
        if self.outline[0] != 0:
            pygame.draw.rect(self.G.WIN, self.outline[1], pygame.Rect(x, y, *self.size), self.outline[0], 3)
        
        return calls
    
    def Abort(self):
        self.G.Abort()

class PresetFrame(BaseFrame):
    """
A Preset Frame! This should not be used directly, but instead used as a parent for subclasses!

## TO USE:
- Override the `__init__` method, e.g.;
```python
def __init__(self, G, pos: GO.P___):
    super().__init__(G, pos, outline=10) # This defines the outline, background and initial size of the frame, you can change this here!
```
<br>
    - You can add paramaters to this if you want to add some things to the class, which you can use in the `_init_objects` method! (if you initialised them *before* the super() call)
    - If you do not implement this, you will be able to change these values by default, which may not be what you want; so it's better to implement this.
- Override the `_init_objects` method, e.g.;
```python
def _init_objects(self):
    self.layers[0].add('main')
    self['main'].append(GUI.Text(self, GO.PCTOP, 'HELLO!'))
```
- Optionally override the _update function like so:
```python
def _update(self, mousePos, events):
    # Code here will run before the elements get updated and the window is drawn.
    return super()._update(mousePos, events)
    # Code here is after the elements have been updated and the window is drawn to the screen.
```
- Use your new class like any other element!

If you want to resize the frame to fit any objects, you can either;
 - Set `self.sizeOfScreen` to the desired size
 - Run `self.fitObjects()` to do that for you
 - Do the resizing, then the fitObjects. This is for when you have objects that attach to the sides of the screen and such.
    """
    def __init__(self, 
                 G, 
                 pos: GO.P___, 
                 initialSze: Iterable[int] = (0, 0),
                 outline: int = 0, 
                 outlinecol: GO.C___ = GO.CGREY, 
                 bgcol: GO.C___ = GO.CWHITE
        ):
        """
        A Frame you can preset! Please see this class' docstring for info on how to use.

        Args:
            G (Graphic): The graphic screen to attach to.
            pos (GO.P___): The position of this object in the Graphic screen.
            outline (int, optional): The thickness of the outline of the element. Defaults to 0.
            outlinecol (GO.C___, optional): The colour of the outline. Defaults to GO.CGREY.
            bgcol (GO.C___, optional): The background colour to the new Graphic-like object. Defaults to GO.CWHITE.
        """
        super().__init__(G, pos, initialSze, outline, outlinecol, bgcol)
        self._init_objects()
        self.fitObjects()
    
    def fitObjects(self):
        """
        Sets the size of the screen to contain every object.

        For objects that snap to the sides of the screen, mostly the right, you may have to set self.sizeOfScreen before or instead of this to get consistant results.
        """
        if len(self.Stuff) == 0:
            self.sizeOfScreen = (0, 0)
            return
        poss = [i.stackP() for i in self.Stuff]
        szes = [i.size for i in self.Stuff]
        mn = (
            min(p[0] for p in poss),
            min(p[1] for p in poss)
        )
        ns = (
            max(p[0]+s[0]-mn[0] for p, s in zip(poss, szes)),
            max(p[1]+s[1]-mn[1] for p, s in zip(poss, szes)),
        )
        self.sizeOfScreen = self.size = ns
    
    def _init_objects(self):
        """
        Initialise all the objects that make up this frame.
        ```python
        def _init_objects(self):
            self.layers[0].add('main')
            self['main'].append(GUI.Text(self, GO.PCTOP, 'HELLO!'))
        ```
        """
        pass
    

class PopupFrame(BaseFrame):
    def __init__(self, 
                 G, 
                 pos: GO.P___, 
                 size: Iterable[int], 
                 outline: int = 10, 
                 outlinecol: GO.C___ = GO.CGREY, 
                 bgcol: GO.C___ = GO.CWHITE
        ):
        """
        A popup frame.

        Args:
            G (Graphic): The Graphic object to add this to.
            pos (GO.P___): The position of this object in the Graphic screen.
            size (Iterable[int]): The size of the screen
            outline (int, optional): The thickness of the outline of the element. Defaults to 10.
            outlinecol (GO.C___, optional): The colour of the outline. Defaults to GO.CGREY.
            bgcol (GO.C___, optional): The background colour to the new Graphic-like object. Defaults to GO.CWHITE.
        """
        super().__init__(G, pos.copy(), size, outline, outlinecol, bgcol)

class ScrollableFrame(BaseFrame):
    def __init__(self, 
                 G, 
                 pos: GO.P___, 
                 goalrect: Iterable[int], 
                 sizeOfScreen: Iterable[int], 
                 outline: int = 10, 
                 bar: bool = True, 
                 outlinecol: GO.C___ = GO.CGREY, 
                 multi: float = 15,
                 decay: float = 0.6,
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
            multi (float, optional): The multiplier of the scroll. Defaults to 15.
            decay (float, optional): The decay of the scroll. Defaults to 0.6.
            bgcol (GO.C___, optional): The background colour to the new Graphic-like object. Defaults to GO.CWHITE.
        """
        super().__init__(G, pos, goalrect, outline, outlinecol, bgcol)
        self.WIN = pygame.Surface(sizeOfScreen)
        self.bar = bar
        self.scroll = [0, 0]
        self.scrollvel = [0, 0]
        self.decay = decay
        self.multi = multi
        self.lastScroll = None
    
    def _update(self, mousePos, events):
        mouseColliding = pygame.Rect(*self.stackP(), *self.size).collidepoint(mousePos)
        if mouseColliding and not self.G.pause:
            for ev in events:
                if ev.type == pygame.MOUSEWHEEL:
                    y = ev.y
                    x = -ev.x
                    multi = 1 if self.lastScroll is None else 1-(time() - self.lastScroll)
                    multi = max(0.1, multi)
                    self.scrollvel[0] += x * self.multi * multi
                    self.scrollvel[1] += y * self.multi * multi
                    self.lastScroll = time()
        self.scroll[0] += self.scrollvel[0]
        self.scroll[1] += self.scrollvel[1]
        self.scrollvel[0] *= self.decay
        self.scrollvel[1] *= self.decay
        self.scroll[0] = min(max(-self.sizeOfScreen[0]+self.size[0], self.scroll[0]), 0)
        self.scroll[1] = min(max(-self.sizeOfScreen[1]+self.size[1], self.scroll[1]), 0)
        x, y = self.stackP()
        self.WIN.fill(self.bgcol)
        mp = (mousePos[0]-x-self.scroll[0], mousePos[1]-y-self.scroll[1])
        if not mouseColliding:
            mp = (Infinity(mp[0]), Infinity(mp[1]))
        calls = self._updateStuff(mp, events)
        self.G.WIN.blit(self.WIN, (x, y), pygame.Rect(-self.scroll[0], -self.scroll[1], *self.size))
        if self.outline[0] != 0:
            pygame.draw.rect(self.G.WIN, self.outline[1], pygame.Rect(x, y, *self.size), self.outline[0], 3)
        if self.bar:
            if self.outline[0] != 0:
                if self.sizeOfScreen[0] > self.size[0]:
                    h = (self.size[0] / self.sizeOfScreen[0]) * self.size[0]
                    p = (x + ((-self.scroll[0]) / self.sizeOfScreen[0]) * self.size[0]+h/2, y + self.size[1] - self.outline[0])
                    pygame.draw.rect(self.G.WIN, (200, 50, 50), (p[0] - h / 2, p[1], h, self.outline[0]), border_radius=5)
                if self.sizeOfScreen[1] > self.size[1]:
                    h = (self.size[1] / self.sizeOfScreen[1]) * self.size[1]
                    p = (x + self.size[0] - self.outline[0], y + ((-self.scroll[1]) / self.sizeOfScreen[1]) * self.size[1]+h/2)
                    pygame.draw.rect(self.G.WIN, (200, 50, 50), (p[0], p[1] - h / 2, self.outline[0], h), border_radius=5)
        return calls

class ScaledByFrame(BaseFrame):
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
        A frame that scales the surface by a certain amount. It dynamically creates a window that is your specified size / scale to put the elements on.

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
        for elm in self.get():
            elm.stackP.winSze = self.sizeOfScreen
    
    def _update(self, mousePos, events):
        x, y = self.stackP()
        self.WIN.fill(self.bgcol)
        mp = ((mousePos[0]-x)/self._scale, (mousePos[1]-y)/self._scale)
        if not pygame.Rect(x, y, *self.size).collidepoint(mousePos):
            mp = (Infinity(mp[0]), Infinity(mp[1]))
        calls = self._updateStuff(mp, events)
        self.G.WIN.blit(pygame.transform.scale(self.WIN, self.size), (x, y))
        if self.outline[0] != 0:
            pygame.draw.rect(self.G.WIN, self.outline[1], pygame.Rect(x, y, *self.size), self.outline[0], 3)
        return calls

class LayoutPos(GO.POverride):
    def __init__(self, layout):
        self.layout = layout
    
    @property
    def idx(self):
        for i in range(len(self.layout.grid)):
            if self.elm in self.layout.grid[i]:
                return (i, self.layout.grid[i].index(self.elm))
        raise IndexError("Element not found in layout grid!")

    def copy(self):
        return LayoutPos(self.layout)
    
    def __call__(self):
        idx = self.idx
        ms = self.layout.max_size
        return (idx[1]*ms[0]+(ms[0]-self.elm.size[0])*self.layout.weights[1].w, idx[0]*ms[1]+(ms[1]-self.elm.size[1])*self.layout.weights[0].w)

class BaseLayout(Element):
    type = GO.TLAYOUT
    def __init__(self, 
                 G, 
                 pos: GO.P___, 
                 size: Iterable[int], 
                 gap: int = 5,
                 outline: int = 0, 
                 outlinecol: GO.C___ = GO.CGREY, 
                 updownWeight: GO.SW__ = GO.SWMID,
                 leftrightWeight: GO.SW__ = GO.SWMID,
                 bgcol: GO.C___ = GO.CWHITE
                ):
        """
        The base Layout object from which many other Layouts are made from.

        Args:
            G (Graphic): The Graphic object to add this to.
            pos (GO.P___): The position of this object in the Graphic screen.
            size (Iterable[int]): The size of the screen.
            gap (int, optional): The gap between each element in the layout. Defaults to 5.
            outline (int, optional): The thickness of the outline of the element. Defaults to 0 (off).
            outlinecol (GO.C___, optional): The colour of the outline. Defaults to GO.CGREY.
            updownWeight (GO.SW__, optional): The vertical weighting of each element in the layout. Defaults to GO.SWMID.
            leftrightWeight (GO.SW__, optional): The horizontal weighting of each element in the layout. Defaults to GO.SWMID.
            bgcol (GO.C___, optional): The background colour to the new Graphic-like object. Defaults to GO.CWHITE.
        """
        super().__init__(G, pos, size)
        self.WIN = pygame.Surface(size)
        self.bgcol = bgcol
        self.outline = (outline, outlinecol)
        self.grid = [[]]
        self.gap = gap / 2
        self.weights = [updownWeight, leftrightWeight]
        self.LP = LayoutPos(self)
    
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
        self.size = newSze
        self.WIN = pygame.Surface(newSze)
        for elm in self.get():
            elm.stackP.winSze = newSze
    
    @property
    def max_size(self):
        alls = self.get()
        if alls == []:
            return 0, 0
        return max(i.size[0] for i in alls)+self.gap*2, max(i.size[1] for i in alls)+self.gap*2
    
    def update(self, mousePos, events, force_redraw=False):
        if force_redraw:
            return self._update(mousePos, events)
        else:
            return ReturnState.REDRAW_HIGH
    
    def _update(self, mousePos, events):
        x, y = self.stackP()
        self.WIN.fill(self.bgcol)
        if pygame.Rect(x, y, *self.size).collidepoint(mousePos):
            mp = (mousePos[0]-x, mousePos[1]-y)
            mouse.Mouse.set(mouse.MouseState.NORMAL)
        else:
            mp = (Infinity(mousePos[0]-x), Infinity(mousePos[1]-y))
        
        calls = self._updateStuff(mp, events)
        self.G.WIN.blit(self.WIN, (x, y))
        if self.outline[0] != 0:
            pygame.draw.rect(self.G.WIN, self.outline[1], pygame.Rect(x, y, *self.size), self.outline[0], 3)
        
        return calls
    
    def Abort(self):
        self.G.Abort()

    def _updateStuff(self, mousepos, evnts):
        oldMP = mousepos
        for i in self.get():
            if isinstance(i, GraphicBase) and pygame.Rect(*i.stackP(), *i.size).collidepoint(mousepos):
                mousepos = (Infinity(mousepos[0]), Infinity(mousepos[1]))
                break
        calls = []
        returns = {}
        for i in self.grid:
            for j in i:
                if j is None:
                    continue
                returns[j] = j.update(mousepos, evnts)
                if returns[j] and ReturnState.STOP in returns[j]:
                    return []
        redraw_tops = []
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
                elif ret == ReturnState.REDRAW_HIGH:
                    redraw_tops.append(obj)
        for obj in redraw_tops:
            obj.update(oldMP, evnts.copy(), True) # Redraw on top of LITERALLY everything
        return calls
    
    def get(self):
        return [j for i in self.grid for j in i if j]
    
    def add_row(self, amnt=1):
        row = [None for _ in range(len(self.grid[0]))]
        self.grid.extend([row for i in range(amnt)])
    
    def add_col(self, amnt=1):
        xtra = [None for _ in range(amnt)]
        for i in self.grid:
            i.extend(xtra)
    
    def extend(self, rows, cols):
        self.add_col(cols)
        self.add_row(rows)
    
    def __len__(self):
        return len(self.grid)

    def __iter__(self):
        return iter(self.grid)
    
    def __getitem__(self, key):
        if isinstance(key, (int, slice)):
            return self.grid[key]
        return self.grid[key[0]][key[1]]
    
    def __setitem__(self, key, value):
        self.grid[key[0]][key[1]] = value

class GridLayout(BaseLayout):
    def __init__(self, 
                 G, 
                 pos: GO.P___, 
                 gap: int = 5,
                 gridSze: Iterable[int] = None,
                 outline: int = 0, 
                 outlinecol: GO.C___ = GO.CGREY, 
                 size: Iterable[int] = None, 
                 updownWeight: GO.SW__ = GO.SWMID,
                 leftrightWeight: GO.SW__ = GO.SWMID,
                 bgcol: GO.C___ = GO.CWHITE
                ):
        """
        A grid layout!

        Args:
            G (Graphic): The Graphic object to add this to.
            pos (GO.P___): The position of this object in the Graphic screen.
            gap (int, optional): The gap between each element in the layout. Defaults to 5.
            gridSze (Iterable[int], optional): The size of the grid. Defaults to None (auto generate).
            outline (int, optional): The thickness of the outline of the element. Defaults to 0 (off).
            outlinecol (GO.C___, optional): The colour of the outline. Defaults to GO.CGREY.
            size (Iterable[int]): The size of the screen, or None to auto adjust the size. Defaults to None.
            updownWeight (GO.SW__, optional): The vertical weighting of each element in the layout. Defaults to GO.SWMID.
            leftrightWeight (GO.SW__, optional): The horizontal weighting of each element in the layout. Defaults to GO.SWMID.
            bgcol (GO.C___, optional): The background colour to the new Graphic-like object. Defaults to GO.CWHITE.
        """
        self.autoAdjust = size is None
        self.gridSze = gridSze
        super().__init__(G, pos, size or (0, 0), gap, outline, outlinecol, updownWeight, leftrightWeight, bgcol)
    
    @property
    def max_size(self):
        return self.gridSze or super().max_size
    
    def adjustSize(self):
        if self.autoAdjust:
            ms = self.max_size
            self.sizeOfScreen = (ms[0]*len(self.grid[0]), ms[1]*len(self.grid))
    
    def update(self, mousePos, events, force_redraw=False):
        self.adjustSize()
        return super().update(mousePos, events, force_redraw)

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
