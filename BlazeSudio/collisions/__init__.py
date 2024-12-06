import os as _os
if 'debugCollisions' in _os.environ:
    from BlazeSudio.collisions.lib.collisions import *
else:
    from BlazeSudio.collisions.generated.collisions import *
