# All about `graphics/graphics.py`
## What it is
This file is really just a very easy way for anyone to make nice graphic screens. Let's go look at how it works!
## Imports
The stuff at the top of the file. You need to:
```py
import graphics.graphics_options as GO # Easy way of calling it
from graphics import Graphic # Imports the thing that we are using
G = Graphic() # makes a new graphics class to use :)
```
## The basics
All it really is is just a preset function that calls your function whenever something happens.

The following is a blank scaffold you can use (or you can use the one at the bottom of graphics.py that has the comments):
```py
@G.Graphic
def funcname(event, *args, element=None, aborted=False, **kwargs):
    if event == GO.EFIRST:
        pass
    elif event == GO.ELOADUI:
        G.Clear()
    elif event == GO.ETICK:
        return True
    elif event == GO.EELEMENTCLICK:
        pass
    elif event == GO.EEVENT:
        pass
    elif event == GO.ELAST:
        pass
```

What the above is is just makes a new function that just shows an (almost, it has the terminal bar at the bottom) white screen.

You can add new things by adding it to the `elif event == GO.ELOADUI:` section like so:

```py
elif event == GO.ELOADUI:
    G.Clear() # This is needed to clear the screen each time
    G.add_text(
        'HI', # The text.
        GO.CGREEN, # The text colour. See below.
        GO.PCCENTER, # The text position. Also see below.
        GO.FTITLE # The text font. Also see below.
    )
```

Now, the things I said above to see here are because you can change them, and I will show you how.

GO to `graphics/graphics_options.py` and look at the `Positions` section (or another section, see the others)

# TODO: THIS AND OTHER DOCS
