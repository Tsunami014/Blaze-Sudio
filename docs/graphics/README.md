# All about `graphics/graphics.py`
## What it is
This file is really just a very easy way for anyone to make nice graphic screens. Let's go look at how it works!
## Imports
The stuff at the top of the file. You need to:
```py
import BlazeSudio.graphics.options as GO # Easy way of calling it
from BlazeSudio.graphics import Graphic # Imports the thing that we are using
G = Graphic() # makes a new graphics class to use :)
```
## The basics
All it really is is just a preset function that calls your function whenever something happens.

[Here](#scaffolds) are some scaffolds you can use or reference as you read everything.

### TO NOTE:
You don't need to specify ANY of these functions if you don't use them.
GO.ETICK: Return False if you want to quit the Graphic screen. This is not needed if you never want to do this.
GO.ELOADUI: Even THIS is not needed, as you can load UI in EFIRST and you may have no need for this
GO.EELEMENTCLICK: Passed 'element'
GO.EEVENT: Passed 'element' (but is event)
GO.ELAST: Passed 'aborted'. Whatever you return here will be returned by the function

### Basics of adding things to the UI
What the above is is just makes a new function that just shows an (almost, it has the terminal bar at the bottom) white screen.

You can add new things by adding it to the `elif event == GO.ELOADUI:` (Or the `E.EFIRST` as said above) section like so:

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

GO to `graphics/options.py` and look at the `Positions` section (or another section, see the others)

# TODO: THIS AND OTHER DOCS

# Scaffolds:
## Blank scaffold:
```py
@G.Graphic
def funcname(event, *args, element=None, aborted=False, **kwargs):
    if event == GO.EFIRST:
        pass
    elif event == GO.ELOADUI:
        G.Clear()
    elif event == GO.ETICK:
        pass
    elif event == GO.EELEMENTCLICK:
        pass
    elif event == GO.EEVENT:
        pass
    elif event == GO.ELAST:
        pass
```
## Commented scaffold:
```py
# Args and kwargs are passed through from the initial call of the func
@G.Graphic # If you use classes, make this CGraphics and add a `self` argument to the function (i.e. def funcname(self, event, *args, etc.))
def funcname(event, *args, element=None, aborted=False, **kwargs):
    if event == GO.EFIRST:
        pass
    elif event == GO.ELOADUI:
        G.Clear()
    elif event == GO.ETICK:
        return True # Return whether or not the loop should continue.
    elif event == GO.EELEMENTCLICK: # Passed 'element'
        pass
    elif event == GO.EEVENT: # Passed 'element' (but is event)
        pass
    elif event == GO.ELAST: # Passed 'aborted'
        pass # Whatever you return here will be returned by the function
```