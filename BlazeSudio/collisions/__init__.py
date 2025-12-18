"""
A collisions library written by Tsunami014 in Python and compiled using Cython to make it super fast!! :)

Every function or method that uses an external library will say so (unless it is obvious, e.g. `shapelyToColl` or `drawShape`), and NONE of the Shape classes do that.

## **BE CAREFUL WITH THE ROTATE FUNCTIONS AND ALWAYS CHECK WHAT VALUE (degrees or radians) THEY ACCEPT!!!**
"""
from BlazeSudio.speed import _COMPILING
if not _COMPILING:
    from .Draw import *
    from .Combine import *
    from .shapely import *
    from .core import *
