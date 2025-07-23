"""
```py
from BlazeSudio.debug import speedup
```
is equivalent to
```py
from BlazeSudio import speedup
speedup.setSpeedupType(1)
```

This makes it always compile functions wherever possible.
"""
from BlazeSudio.speedup import *
setSpeedupType(1)
