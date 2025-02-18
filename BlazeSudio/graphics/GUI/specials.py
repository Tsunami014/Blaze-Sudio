import pygame
import inspect
from typing import Iterable
from time import time
from difflib import get_close_matches
from BlazeSudio.graphics import mouse, options as GO
from BlazeSudio.graphics.base import Element, ReturnState
from BlazeSudio.graphics import GUI
from BlazeSudio.graphics.stacks import Stack
from BlazeSudio.graphics.stuff import Collection

__all__ = [
    'TerminalBar',
    'DebugTerminal',
    'ScrollableFrame',
    'ScaledByFrame',
    'PopupFrame',
    'GridLayout',

    'PresetFrame',

    'BaseFrame',
    'BaseLayout',
    'GraphicBase',

    'LayoutPos',
    'MousePos'
]

class MousePos:
    """Mouse positioning which holds it's real position"""
    def __init__(self, x: int, y: int):
        self._pos = [x, y]
        self.outOfRange = False
    
    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, new: Iterable):
        if not isinstance(new, Iterable):
            raise TypeError(
                'New position is not iterable!'
            )
        if len(new) != 2:
            raise ValueError(
                f'New position has {len(new)} items, when it should have 2!'
            )
        self._pos = [new[0], new[1]]
    
    def copy(self) -> 'MousePos':
        n = MousePos(*self._pos)
        n.outOfRange = self.outOfRange
        return n
    
    def __len__(self):
        return 2
    
    def __bool__(self):
        return not self.outOfRange
    
    def __getitem__(self, idx: int) -> int:
        if self.outOfRange:
            raise ValueError(
                'Mouse position is out of window, cannot get the value!'
            )
        return self._pos[idx]
    
    def __setitem__(self, idx: int, newval: int) -> int:
        if self.outOfRange:
            raise ValueError(
                'Mouse position is out of window, cannot get the value!'
            )
        self._pos[idx] = newval
    
    def __iter__(self) -> iter:
        if self.outOfRange:
            raise ValueError(
                'Mouse position is out of window, cannot get the value!'
            )
        return iter(self._pos)
    
    def __str__(self):
        if self.outOfRange:
            return f'Mouse out of window. Real pos; ({self._pos[0]}, {self._pos[1]})'
        return f'({self._pos[0]}, {self._pos[1]})'
    def __repr__(self): return str(self)

class GraphicBase:
    """This contains all the things an object needs to be a graphic object and is not meant to be used directly."""
    # Stuff that needs replacing with instance (not class) variables (but have been provided as instants just coz):
    WIN: pygame.Surface = pygame.Surface((0, 0))
    size: tuple[int, int] = (0, 0)
    stacks: Stack = Stack()
    pause: bool = False

    def __init__(self):
        self.Stuff: Collection = Collection(self)

    # Functions that need replacing:
    def Abort(self):
        pass

    # Things that don't need replacing:
    def _updateStuff(self, mousepos, evnts):
        calls = []
        oldMP = mousepos
        for lay in self.Stuff.layers:
            mousepos = oldMP.copy()
            if not mousepos.outOfRange:
                for i in lay:
                    if isinstance(i, GraphicBase) and pygame.Rect(*i.stackP(), *i.size).collidepoint(*mousepos):
                        mousepos.outOfRange = True
                        break
            redraw_tops = []
            redraw_vtops = []
            # TODO: Have return states able to be passed down instead of just the calls
            def handle_returns(returns, care4Redraw=False):
                if returns is None:
                    return
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
                                obj.UpdateDraw(mousepos.copy(), evnts.copy(), True) # Redraw forcefully on top of everything else
                            elif ret == ReturnState.REDRAW_HIGH:
                                redraw_tops.append(obj)
                            elif ret == ReturnState.REDRAW_HIGHEST:
                                redraw_vtops.append(obj)
            handle_returns(lay.update(mousepos, evnts.copy()), True)
            moreRets = {}
            for obj in redraw_tops:
                moreRets[obj] = obj.UpdateDraw(mousepos.copy(), evnts.copy(), True) # Redraw on top of everything
            for obj in redraw_vtops:
                moreRets[obj] = obj.UpdateDraw(oldMP.copy(), evnts.copy(), True) # Redraw on top of LITERALLY everything
                # Very top redraws also get original mouse position!
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

    def insert_layer(self, pos=None):
        """
        Inserts a blank layer into the Stuff.

        Args:
            pos (int, optional): The position to put the new layer. Defaults to the end of the list (None).
        
        Pos:
            - Negative indexes act *kinda* like negative list indexes; -1 = second last, -2 = third last, etc.
            - None places it last
            - Positive indexes place it where you would expect; 0 = first, 1 = second, etc.
            - **The lower down (i.e. index closer to 0) the layer is, the later it will be rendered** (the layer with index 1 will be rendered before the layer of index 0)

        Returns:
            Stuff: The newly created layer
        """
        return self.Stuff.insert_layer(pos)

class BaseFrame(GraphicBase, Element):
    type = GO.TFRAME
    def __init__(self, 
                 pos: GO.P___, 
                 size: Iterable[int], 
                 outline: int = 10, 
                 outlinecol: GO.C___ = GO.CGREY, 
                 bgcol: GO.C___ = GO.CWHITE
                ):
        """
        The base Frame object from which many other Frames are made from.

        Args:
            pos (GO.P___): The position of this object in the Graphic screen.
            size (Iterable[int]): The size of the screen
            outline (int, optional): The thickness of the outline of the element. Defaults to 10.
            outlinecol (GO.C___, optional): The colour of the outline. Defaults to GO.CGREY.
            bgcol (GO.C___, optional): The background colour to the new Graphic-like object. Defaults to GO.CWHITE.
        """
        GraphicBase.__init__(self)
        Element.__init__(self, pos, size)
        self.WIN = pygame.Surface(size)
        self.bgcol = bgcol
        self.outline = (outline, outlinecol)
        self.stacks = Stack()
        self.Stuff = Collection(self)
    
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
        coll = pygame.Rect(x, y, *self.size).collidepoint(*mousePos.pos)
        mousePos.pos = (mousePos.pos[0]-x, mousePos.pos[1]-y)
        if coll:
            mouse.Mouse.set(mouse.MouseState.NORMAL)
        mousePos.outOfRange = not coll
        
        calls = self._updateStuff(mousePos, events)
        self.G.WIN.blit(self.WIN.subsurface((0, 0, *self.size)), (x, y))
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
def __init__(self, pos: GO.P___):
    super().__init__(pos, outline=10) # This defines the outline, background and initial size of the frame, you can change this here!
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
                 pos: GO.P___, 
                 initialSze: Iterable[int] = (0, 0),
                 outline: int = 0, 
                 outlinecol: GO.C___ = GO.CGREY, 
                 bgcol: GO.C___ = GO.CWHITE
        ):
        """
        A Frame you can preset! Please see this class' docstring for info on how to use.

        Args:
            pos (GO.P___): The position of this object in the Graphic screen.
            outline (int, optional): The thickness of the outline of the element. Defaults to 0.
            outlinecol (GO.C___, optional): The colour of the outline. Defaults to GO.CGREY.
            bgcol (GO.C___, optional): The background colour to the new Graphic-like object. Defaults to GO.CWHITE.
        """
        super().__init__(pos, initialSze, outline, outlinecol, bgcol)
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
                 pos: GO.P___, 
                 size: Iterable[int], 
                 outline: int = 10, 
                 outlinecol: GO.C___ = GO.CGREY, 
                 bgcol: GO.C___ = GO.CWHITE
        ):
        """
        A popup frame.

        Args:
            pos (GO.P___): The position of this object in the Graphic screen.
            size (Iterable[int]): The size of the screen
            outline (int, optional): The thickness of the outline of the element. Defaults to 10.
            outlinecol (GO.C___, optional): The colour of the outline. Defaults to GO.CGREY.
            bgcol (GO.C___, optional): The background colour to the new Graphic-like object. Defaults to GO.CWHITE.
        """
        super().__init__(pos.copy(), size, outline, outlinecol, bgcol)

class ScrollableFrame(BaseFrame):
    def __init__(self, 
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
        super().__init__(pos, goalrect, outline, outlinecol, bgcol)
        self.WIN = pygame.Surface(sizeOfScreen)
        self.bar = bar
        self.scroll = [0, 0]
        self.scrollvel = [0, 0]
        self.decay = decay
        self.multi = multi
        self.lastScroll = None
    
    def _update(self, mousePos, events):
        mouseColliding = pygame.Rect(*self.stackP(), *self.size).collidepoint(*mousePos.pos)
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
        mousePos.pos = (mousePos.pos[0]-x-self.scroll[0], mousePos.pos[1]-y-self.scroll[1])
        mousePos.outOfRange = not mouseColliding
        calls = self._updateStuff(mousePos, events)
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
            pos (GO.P___): The position of this object in the Graphic screen.
            size (Iterable[int]): The size of the screen.
            scale (int, optional): The scale of the screen. Defaults to 2.
            outline (int, optional): The thickness of the outline of the element. Defaults to 10.
            outlinecol (GO.C___, optional): The colour of the outline. Defaults to GO.CGREY.
            bgcol (GO.C___, optional): The background colour to the new Graphic-like object. Defaults to GO.CWHITE.
        """
        super().__init__(pos, size, outline, outlinecol, bgcol)
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
        coll = pygame.Rect(x, y, *self.size).collidepoint(*mousePos.pos)
        mousePos.pos = ((mousePos.pos[0]-x)/self._scale, (mousePos.pos[1]-y)/self._scale)
        if coll:
            mouse.Mouse.set(mouse.MouseState.NORMAL)
        mousePos.outOfRange = not coll
        calls = self._updateStuff(mousePos, events)
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

class BaseLayout(GraphicBase, Element):
    type = GO.TLAYOUT
    def __init__(self, 
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
            pos (GO.P___): The position of this object in the Graphic screen.
            size (Iterable[int]): The size of the screen.
            gap (int, optional): The gap between each element in the layout. Defaults to 5.
            outline (int, optional): The thickness of the outline of the element. Defaults to 0 (off).
            outlinecol (GO.C___, optional): The colour of the outline. Defaults to GO.CGREY.
            updownWeight (GO.SW__, optional): The vertical weighting of each element in the layout. Defaults to GO.SWMID.
            leftrightWeight (GO.SW__, optional): The horizontal weighting of each element in the layout. Defaults to GO.SWMID.
            bgcol (GO.C___, optional): The background colour to the new Graphic-like object. Defaults to GO.CWHITE.
        """
        GraphicBase.__init__(self)
        Element.__init__(self, pos, size)
        self.WIN = pygame.Surface(size)
        self.bgcol = bgcol
        self.outline = (outline, outlinecol)
        self._grid = [[]]
        self.gap = gap / 2
        self.weights = [updownWeight, leftrightWeight]
        self.LP = LayoutPos(self)
    
    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, newgrid):
        for i in newgrid:
            for it in i:
                if (it is not None) and (not it._init2Ran):
                    it.G = self
                    it._init2()
                    it._init2Ran = True
        self._grid = newgrid
    
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
        coll = pygame.Rect(x, y, *self.size).collidepoint(*mousePos.pos)
        mousePos.pos = (mousePos.pos[0]-x, mousePos.pos[1]-y)
        if coll:
            mouse.Mouse.set(mouse.MouseState.NORMAL)
        mousePos.outOfRange = not coll
        
        calls = self._updateStuff(mousePos, events)
        self.G.WIN.blit(self.WIN, (x, y))
        if self.outline[0] != 0:
            pygame.draw.rect(self.G.WIN, self.outline[1], pygame.Rect(x, y, *self.size), self.outline[0], 3)
        
        return calls
    
    def Abort(self):
        self.G.Abort()

    def _updateStuff(self, mousepos, evnts):
        oldMP = mousepos
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
                            obj.UpdateDraw(mousepos.copy(), evnts.copy(), True) # Redraw forcefully on top of everything else
                        elif ret == ReturnState.REDRAW_HIGH:
                            redraw_tops.append(obj)
                        elif ret == ReturnState.REDRAW_HIGHEST:
                            redraw_vtops.append(obj)
        returns = {}
        for i in self.grid:
            for j in i:
                if j is None:
                    continue
                returns[j] = j.UpdateDraw(mousepos, evnts)
                if returns[j] and ReturnState.STOP in returns[j]:
                    return []
        handle_returns(returns, True)
        moreRets = {}
        for obj in redraw_tops:
            moreRets[obj] = obj.UpdateDraw(mousepos.copy(), evnts.copy(), True) # Redraw on top of everything
        for obj in redraw_vtops:
            moreRets[obj] = obj.UpdateDraw(oldMP.copy(), evnts.copy(), True) # Redraw on top of LITERALLY everything
            # Very top redraws also get original mouse position!
        handle_returns(moreRets)
        return calls
    
    def get(self):
        return [j for i in self.grid for j in i if j]
    
    def add_row(self, amnt=1):
        row = [None for _ in range(len(self.grid[0]))]
        self.grid.extend([row for _ in range(amnt)])
    
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
        super().__init__(pos, size or (0, 0), gap, outline, outlinecol, updownWeight, leftrightWeight, bgcol)
    
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
    def __init__(self, spacing=5, prefix='> ', cursor='_'):
        """
        Adds a terminal bar to the bottom of your screen! You can use this for debugging and can run commands using it also for debugging!
        Or just have it as a feature in your game!

        Args:
            spacing (int, optional): The spacing between the text and the top and bottom of the bar. Defaults to 5.
            prefix (str, optional): The prefix of the terminal. Defaults to '> '.
            cursor (str, optional): The cursor of the terminal. Defaults to '_'.
        """
        self.spacing = spacing
        r = GO.FCODEFONT.render('> ', GO.CWHITE)
        h = r.get_height()+self.spacing*2
        super().__init__(lambda: (0, self.G.WIN.get_height()-h), (0, h))
        self.active = -1
        self.txt = ''
        self.prefix = prefix
        self.cur = cursor
        self._onEnters = []
    
    def _init2(self):
        self.size = (self.G.WIN.get_width(), self.size[1])
        super()._init2()
    
    def onEnter(self, func):
        self._onEnters.append(func)
        return func
    
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
    
    def update(self, mousePos, events, force_redraw=False):
        if not force_redraw:
            return ReturnState.REDRAW_HIGHEST

        if not self.G.pause:
            if self.collides(*mousePos.pos):
                mouse.Mouse.set(mouse.MouseState.TEXT)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if self.active != -1:
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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and not self.G.pause:
                    if event.button == pygame.BUTTON_LEFT:
                        self.toggleactive(not self.collides(*mousePos.pos))
        
        if self.active >= 0:
            self.active -= 1
            if self.active <= 0:
                self.active = 60

    def draw(self):
        r = self.render()
        h = r.get_height()+self.spacing*2
        pygame.draw.rect(self.G.WIN, GO.CBLACK, pygame.Rect(0, self.G.WIN.get_height()-h, self.G.WIN.get_width(), h))
        self.G.WIN.blit(r, (self.spacing, self.G.WIN.get_height()-h+self.spacing))
    
    @property
    def height(self):
        return self.render().get_height()+self.spacing*2

    def render(self):
        t = self.prefix+self.txt
        if self.active >= 30:
            t += self.cur
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

class DebugTerminal(TerminalBar):
    def __init__(self, spacing=5, prefix='> ', cursor='_', max_suggests=5, jump_to_shortcut=pygame.K_SLASH):
        """
        Adds a terminal bar to the bottom of your screen! You can set instructions, and it comes with autocomplete, history and error messages!

        Args:
            spacing (int, optional): The spacing between the text and the top and bottom of the bar. Defaults to 5.
            prefix (str, optional): The prefix of the terminal. Defaults to '> '.
            cursor (str, optional): The cursor of the terminal. Defaults to '_'.
            max_suggests (int, optional): The maximum amount of suggestions to show. Defaults to 5.
            jump_to_shortcut (int, optional): The key to press to jump to the terminal. Defaults to pygame.K_SLASH.
        """
        super().__init__(spacing, prefix, cursor)
        self.cmds = {}
        self.history = []
        self.historyIndex = -1
        self.suggestIndex = 0
        self.popup = None
        self._onEnters = None
        self._onWrong = None
        self.maxSuggests = max_suggests
        self.jumpShort = jump_to_shortcut
    
    def onEnter(self, func):
        """Only used if doesn't start with `/` (so not a command)"""
        self._onEnters = func
        return func
    
    def onWrong(self, func):
        """Only used if the command is not found. Takes in an argument of a list of the command and the arguments."""
        self._onWrong = func
        return func
    
    def addCmd(self, name, func):
        """You don't need to add the `/` to the name, it will be added automatically. The name is lowercase. It NEEDS *args. The first non-empty line in it's docstring will be shown."""
        self.cmds[name.lower()] = func
    
    def UpdateDraw(self, mousePos, events, force_redraw=False):
        if not force_redraw:
            return ReturnState.REDRAW_HIGHEST
        if self.popup is not None:
            self.popup.UpdateDraw(mousePos, events, force_redraw)
        return super().UpdateDraw(mousePos, events, force_redraw)
    
    def _delPopup(self):
        self.popup = None
    
    def makePopup(self):
        self.popup = PopupFrame(self.G, GO.PCCENTER, (0, 0), 5)
        self.popup.layers[0].add('Main')
        self.popup['Main'].append(GUI.Button(self.popup, GO.PRTOP, GO.CRED, '❌', func=self._delPopup))
        return self.popup['Main']
    
    def _resizePopup(self):
        self.popup.sizeOfScreen = self.popup.size = (max(e2.size[0] for e2 in self.popup['Main'])+self.popup['Main'][0].size[0]+20, sum(e.size[1] for e in self.popup['Main'][1:])+10)
    
    def update(self, mousePos, events, force_redraw=False):
        for event in events.copy():
            if event.type == pygame.KEYDOWN:
                if event.type in (
                    pygame.K_LSHIFT, pygame.K_RSHIFT, 
                    pygame.K_LCTRL, pygame.K_RCTRL, 
                    pygame.K_LALT, pygame.K_RALT, 
                    pygame.K_LMETA, pygame.K_RMETA, 
                    pygame.K_LSUPER, pygame.K_RSUPER,
                    pygame.K_CAPSLOCK, pygame.K_NUMLOCK,
                ):
                    del events[events.index(event)]
                    continue
                self._delPopup()
                if event.key == self.jumpShort:
                    doneSmthn = False
                    if self.active < 0:
                        self.active = 60
                        doneSmthn = True
                    if self.txt == "":
                        self.txt = "/"
                        doneSmthn = True
                    if doneSmthn:
                        del events[events.index(event)]
                        continue
                elif self.active != -1:
                    if event.key == pygame.K_TAB:
                        if (not self.txt.startswith("/")) or ' ' in self.txt:
                            del events[events.index(event)]
                            continue
                        suggests = self.suggests()
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            self.suggestIndex += 1
                            if self.suggestIndex >= len(suggests):
                                self.suggestIndex = 0
                        else:
                            if self.historyIndex != -1:
                                self.historyIndex = -1
                                self.history.pop()
                            self.txt = '/'+suggests[self.suggestIndex]
                            self.suggestIndex = 0
                        del events[events.index(event)]
                        continue
                    else:
                        self.suggestIndex = 0
                    if event.key == pygame.K_RETURN:
                        if self.txt.startswith("/"):
                            args = self.txt[1:].split(' ')
                            cmd = args[0].lower()
                            if cmd in self.cmds:
                                func = self.cmds[cmd]
                                passArgs = [a for a in args[1:] if a]
                                error = False
                                args = inspect.getfullargspec(func)
                                if args.varargs is None:
                                    numargs = len(args.args)
                                    defaults = numargs-len(args.defaults or [])
                                    if inspect.isclass(func):
                                        numargs -= 1 # For the 'self' argument
                                    if not (defaults <= len(passArgs) <= numargs):
                                        error = True
                                        pop = self.makePopup()
                                        LTOP = GO.PNEW((0, 0), (0, 1))
                                        if defaults == numargs:
                                            pop.extend([
                                                GUI.Empty(self.popup, LTOP, (10, 10)),
                                                GUI.Text(self.popup, LTOP, f"Command '/{cmd}' requires {defaults} arguments but was provided {len(passArgs)}!"),
                                            ])
                                        else:
                                            pop.extend([
                                                GUI.Empty(self.popup, LTOP, (10, 10)),
                                                GUI.Text(self.popup, LTOP, f"Command '/{cmd}' requires {defaults} - {numargs} arguments but was provided {len(passArgs)}!"),
                                            ])
                                        self._resizePopup()
                                if not error:
                                    func(*passArgs)
                            else:
                                opts = get_close_matches(cmd, self.cmds.keys(), n=3, cutoff=0.35) # n=self.maxSuggests
                                pop = self.makePopup()
                                LTOP = GO.PNEW((0, 0), (0, 1))
                                pop.extend([
                                    GUI.Empty(self.popup, LTOP, (10, 10)),
                                    GUI.Text(self.popup, LTOP, f"Command '/{cmd}' not found!"),
                                ])
                                if self._onWrong is not None:
                                    self._onWrong(args)
                                if opts:
                                    rainbow = GO.CRAINBOW()
                                    def doIt(i):
                                        self.set('/'+i+' ')
                                        self._delPopup()
                                        self.active = -2
                                    pop.extend([
                                        GUI.Text(self.popup, LTOP, "Did you mean: ")
                                    ] + [
                                        GUI.Button(self.popup, LTOP, next(rainbow), f"  '{i}'", func=lambda i=i: doIt(i))
                                        for i in opts
                                    ])
                                self._resizePopup()
                        else:
                            if self._onEnters is not None:
                                self._onEnters(self.txt)
                        if self.historyIndex != -1:
                            self.history[-1] = self.txt
                        else:
                            self.history.append(self.txt)
                        if self.txt.startswith("/"):
                            self.active = -1
                        self.txt = ""
                        del events[events.index(event)]
                    elif event.key == pygame.K_UP:
                        if self.historyIndex == -1:
                            self.history.append(self.txt)
                            self.historyIndex = len(self.history)-2
                        else:
                            self.historyIndex = max(0, self.historyIndex-1)
                        self.txt = self.history[self.historyIndex]
                    elif event.key == pygame.K_DOWN:
                        if self.historyIndex == -1:
                            self.txt = ''
                            continue
                        self.historyIndex += 1
                        if self.historyIndex >= len(self.history)-1:
                            self.historyIndex = -1
                            self.txt = self.history.pop()
                        else:
                            self.txt = self.history[self.historyIndex]
                    else:
                        if self.historyIndex != -1:
                            self.historyIndex = -1
                            self.history.pop()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and not self.G.pause:
                if self.active == -2:
                    self.active = 60
                    del events[events.index(event)]
                self._delPopup()

        return super().update(mousePos, events, force_redraw)

    def suggests(self):
        if (not self.txt.startswith("/")) or ' ' in self.txt:
            return []
        t = self.txt[1:].lower()
        suggests = [k for k in self.cmds if k.startswith(t)]
        def order(suggests):
            seen = set()
            unique_list = []
            for item in suggests:
                if item not in seen:
                    unique_list.append(item)
                    seen.add(item)
            return unique_list
        if len(suggests) < self.maxSuggests:
            suggests.extend(get_close_matches(t, self.cmds.keys(), n=self.maxSuggests, cutoff=0.4))
            suggests = order(suggests)
        if len(suggests) < self.maxSuggests:
            suggests.extend([k for k in self.cmds if t.startswith(k)])
            suggests = order(suggests)
        if len(suggests) < self.maxSuggests:
            suggests.extend([k for k in self.cmds if t in k])
            suggests = order(suggests)
        return suggests[:self.maxSuggests]

    def draw(self):
        super().draw()
        if self.active >= 0 and self.maxSuggests > 0 and self.txt.startswith("/"):
            cmd = self.txt.split(' ')[0].lower()[1:]
            if ' ' in self.txt:
                if cmd in self.cmds:
                    doc = [i for i in self.cmds[cmd].__doc__.split('\n') if i]
                    if doc:
                        suggests = [doc[0].strip()]
                    else:
                        suggests = ['/'+cmd]
                    self.suggestIndex = 0
                else:
                    suggests = []
            else:
                suggests = []
                for val in self.suggests():
                    if val == self.txt[1:]:
                        suggests = ['/'+cmd] + suggests
                    else:
                        suggests.append('/'+val)
                
                if suggests:
                    doc = [i for i in self.cmds[suggests[self.suggestIndex][1:]].__doc__.split('\n') if i]
                    if doc:
                        suggests[self.suggestIndex] = doc[0].strip()

            rends = [GO.FCODEFONT.render((' '*len(self.prefix))+sug, (GO.CYELLOW if idx == self.suggestIndex else GO.CWHITE)) for idx, sug in enumerate(suggests)]
            szes = [r.get_size() for r in rends]
            h = self.height
            for idx in range(len(suggests)):
                r = rends[idx]
                th = szes[idx][1]+self.spacing*2
                h += th
                toprad = -1
                if idx < len(suggests)-1:
                    toprad = min(max(szes[idx][0]-szes[idx+1][0], -1), 5)
                else:
                    toprad = min(szes[idx][0], 5)
                botrad = -1
                if idx != 0:
                    botrad = min(max(szes[idx][0]-szes[idx-1][0], -1), 5)
                pygame.draw.rect(self.G.WIN, 
                                 GO.CBLACK, 
                                 pygame.Rect(0, self.G.WIN.get_height()-h, szes[idx][0]+self.spacing*2, th), 
                                 border_top_right_radius=toprad,
                                 border_bottom_right_radius=botrad)
                y = self.G.WIN.get_height()-h+self.spacing
                self.G.WIN.blit(r, (self.spacing, y))
