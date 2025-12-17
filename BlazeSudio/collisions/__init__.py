import os as _os
if _os.environ.get('BSdebugCollisions', '0') == '1':
    from BlazeSudio.collisions.lib.collisions import *
else:
    from BlazeSudio.collisions.generated.collisions import *
