from BlazeSudio.graphics.stacks import StackPart
from BlazeSudio.graphics import options as GO
import inspect
from typing import Any, Iterable, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from BlazeSudio.graphics.GUI import GraphicBase

__all__ = [
    'HiddenStatus', 
    'Element', 
    'ReturnState', 
    'ReturnGroup'
]

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
    G: 'GraphicBase'
    def __init__(self, pos: GO.P___, size: Iterable[int|float]):
        """
        Base element class, do not directly use, but instead subclass to make your own Elements.

        Args:
            pos (GO.P___): The position of this element on the screen. 
            size (Iterable[number, number]): The size of this element.
        """
        self.pos: GO.P___ = pos
        self.hiddenStatus = HiddenStatus.SHOWING
        self.size = size
        self.uid = self.NEXT_UID[0]
        self.NEXT_UID[0] += 1
        self._init2Ran = False
    
    def _init2(self):
        if isinstance(self.pos, GO.POverride):
            self.stackP = self.pos.copy()
            self.stackP.setup(self, self.G)
        else:
            self.stackP = StackPart(self, self.G.stacks, self.pos, self.G.sizeOfScreen)
    
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
        
        if isinstance(ret, (ReturnState, ReturnGroup)):
            if ReturnState.STOP in ret:
                return ret

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
    
    def __getattribute__(self, name: str) -> Any:
        if name == 'size' and 'size' in self.__dict__ and 'hiddenStatus' in self.__dict__ and self.hiddenStatus == HiddenStatus.GONE:
            return (0, 0)
        elif name == ('G', 'stackP') and 'G' not in self.__dict__:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'. This is because you are trying to run something that is trying to access this variable \
when this object has not been initialised yet. Initialise this object first (by e.g. adding it to a `Collection`) before running whatever it was that made this error. \
If you are a developer, try putting whatever code that requires this variable inside `_init2`."
            )
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
