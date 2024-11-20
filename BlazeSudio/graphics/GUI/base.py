from BlazeSudio.graphics.stacks import StackPart
from BlazeSudio.graphics import options as GO
import inspect
from typing import Any, Iterable
from enum import Enum

__all__ = ['HiddenStatus', 'Element', 'ReturnState', 'ReturnGroup']

class HiddenStatus(Enum):
    """Different states an Element can be in relation to drawing and updating"""

    SHOWING = 0
    """Showing, runs normally"""
    NOTUPDATING = 1
    """Rendering, but doesn't update"""
    HIDDEN = 2
    """Not rendering, but still updating and still has size"""
    GONE = 3
    """Not rendering, has no size and doesn't update"""

class Element:
    NEXT_UID = [0]
    type = None
    def __init__(self, G, pos: GO.P___, size: Iterable[int|float]):
        """
        Base element class, do not directly use.

        Args:
            G (Graphic): The graphic screen to put this element on.
            pos (GO.P___): The position of this element on the screen. 
            size (Iterable[number, number]): The size of this element.
        """
        self.G = G
        self.pos: GO.P___ = pos
        self.hiddenStatus = HiddenStatus.SHOWING
        self.size = size
        if isinstance(pos, GO.POverride):
            self.stackP = pos.copy()
            self.stackP.setup(self, G)
        else:
            self.stackP = StackPart(self, G.stacks, pos, size, G.sizeOfScreen)
        self.uid = self.NEXT_UID[0]
        self.NEXT_UID[0] += 1
    
    def remove(self):
        self.stackP.remove()
        self.G.Stuff.remove(self)
    
    def change_pos(self, newPos):
        self.stackP.remove()
        self.pos = newPos
        self.stackP = StackPart(self, self.G.stacks, newPos, self.size, self.G.sizeOfScreen)
    
    def UpdateDraw(self, mousePos, events, force_redraw=False):
        if self.hiddenStatus == HiddenStatus.GONE:
            return
        
        args = inspect.getfullargspec(self.update).args
        ret = None
        if len(args) == 4: # If includes the force_redraw arg then let it update again
            ret = self.update(mousePos.copy(), events, force_redraw)
        elif not force_redraw:
            ret = self.update(mousePos.copy(), events)
        
        if self.hiddenStatus in (HiddenStatus.SHOWING, HiddenStatus.NOTUPDATING):
            args2 = inspect.getfullargspec(self.draw).args
            if len(args2) == 2: # Includes mousepos
                self.draw(mousePos) # We don't use mousePos anymore, no need to copy it this time
            else:
                self.draw()
        
        if ret:
            return ret
        return
    
    # Required subclass functions
    def update(self, mousePos, events):
        pass

    def draw(self):
        pass
    
    def get(self):
        pass
    
    def set(self):
        pass
    
    # Utility functions
    def __eq__(self, other):
        return self.uid == other
    
    def __hash__(self):
        return hash(self.uid)
    
    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if name == 'size' and 'stackP' in self.__dict__: # Safeguard against running this before initialisation of stackP
            self.stackP.setSize(self.size) # Automatically update stackP size whenever you set self.size
    
    def __getattribute__(self, name: str) -> Any:
        if name == 'size' and 'size' in self.__dict__ and 'hiddenStatus' in self.__dict__ and self.hiddenStatus == HiddenStatus.GONE:
            return (0, 0)
        else:
            return super().__getattribute__(name)
    
    def __str__(self):
        return f'<{self.__class__.__name__}({str(self.get())})>'
    def __repr__(self): return str(self)

class ReturnState(Enum):
    # If nothing happpens, return None as usual
    STOP = -1
    """Stop updating any more elements before next frame"""

    ABORT = 1
    """Abort the Graphics screen"""
    
    CALL = 2
    """Call the main graphic screen function on this"""
    
    REDRAW = 3
    """Redraw this element on top of all the others in its layer. Used for buttons and such."""

    REDRAW_HIGH = 4
    """Redraws the element after all the other redraws to become the VERY top. Used for Frames, Grids and other layouts."""""

    REDRAW_HIGHEST = 5
    """Redraws the element after all the other higher redraws to become the *VERY VERY* top. Used for events, e.g. dropdowns, toasts and textboxes."""

    DONTCALL = 6
    """Don't call the graphic screen function on this element"""
    
    def __add__(self, otherState):
        if not isinstance(otherState, (ReturnState, ReturnGroup)):
            raise TypeError(
                'Invalid type for add: %s! Must be a ReturnState or a ReturnGroup!'%str(type(otherState))
            )
        if isinstance(otherState, ReturnGroup):
            otherState.append(self)
            return otherState
        return ReturnGroup(self, otherState)
    
    def __iter__(self):
        return iter((self,))
    
    def __contains__(self, otherState):
        if not isinstance(otherState, (ReturnState, int)):
            raise TypeError(
                'Invalid type for add: %s! Must be a ReturnState or int!'%str(type(otherState))
            )
        if isinstance(otherState, int):
            return self.value == otherState
        return self == otherState

    def get(self):
        return [self]

class ReturnGroup:
    def __init__(self, *states):
        self.states = list(states)
    
    def append(self, otherState):
        self.states.append(otherState)
    
    def get(self):
        return self.states
    
    def __add__(self, otherState):
        if not isinstance(otherState, (ReturnState, ReturnGroup)):
            raise TypeError(
                'Invalid type for add: %s! Must be a ReturnState or a ReturnGroup!'%str(type(otherState))
            )
        if isinstance(otherState, ReturnGroup):
            self.states.extend(otherState.states)
        else:
            self.states.append(otherState)
        return self
    
    def __iter__(self):
        return iter(self.states)
    
    def __contains__(self, otherState):
        if not isinstance(otherState, (ReturnState, int)):
            raise TypeError(
                'Invalid type for add: %s! Must be a ReturnState or int!'%str(type(otherState))
            )
        if isinstance(otherState, int):
            return otherState in [i.value for i in self.states]
        return otherState in self.states
    
    def __str__(self):
        return f'<ReturnGroup with states {self.states}>'
    def __repr__(self): return str(self)
