"""
This uses the not compiled version of the collisions library; useful for debugging.

Use as `from BlazeSudio.debug import collisions` as a drop-in replacement for `from BlazeSudio import collisions`
"""
import os as _os
_os.environ['BSdebugCollisions'] = '1'
from BlazeSudio.collisions import *
