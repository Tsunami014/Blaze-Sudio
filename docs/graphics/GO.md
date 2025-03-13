# About GO (Graphics options)

The graphics options are a bunch of preset things, some of which you can make your own of.

## TO USE

`import BlazeSudio.graphics.options as GO` or `from graphics import options as GO`

You could just go `from BlazeSudio.graphics import options` but GO (Standing for Graphics Options) is cooler and I use it everywhere and it just makes it slightly easier (like `import numpy as np`)

## Table of stuff it has in it
//TODO: update PNEW

| Category | Description | Character | Examples | Special uses |
|:---|:---|:---:|---:|:---|
| Colours   | A colour! | C | `GO.CWHITE`, `GO.CRED` | <li>`GO.CNEW(name:str)` gets the colour name (e.g. `GO.CORANGE` will get an orange colour)</li><li>`GO.CRAINBOW()` will return a thing you can loop around colours by calling <pre>l = GO.CRAINBOW()<br>colour = next(l)<br>different_colour = next(l)</pre></li> |
| Fonts     | A `pygame.Font` | F | `GO.FTITLE`, `GO.FREGULAR` | |
| Positions | A position of an object on the screen (e.g. `GO.PCBOTTOM`=Center BOTTOM) | P | `GO.PCCENTER`, `GO.PCTOP` | <li>`GO.PNEW(stack:list[int, int], func:function)` Makes a new position. See [the reference](#diy-positions) for information on this.</li><li>`GO.PSTATIC(x:int,y:int)` Makes a new static position wherever you specify that you can use the same as the other positions.</li> |
| Events    | An event, used in the [Graphics class](README.md) | E | `GO.ELOADUI`, `GO.ETICK` | |
| Types     | A type of a UI element, used in the [Graphics class](README.md) | T | `GO.TBUTTON`, `GO.TTEXTBOX` | |
| Resizes   | The type of resizing a [textbox](README.md) does | R | `GO.RWIDTH`, `GO.RNONE` | |

***

# Other info

## DIY positions
With the GO.PNEW:

### The `stack` param
This param decides where the next eement placed with the exact position will go.

Let's say for example that you have a position for the bottom right of the screen. This means that you want all the next elements to be to the left of it.

E.g. (If you place down elements A, B and C in order)

```
┌────┐
│    │
│    │
│ CBA│
└────┘
```

So in that case your `stack` param would be `[-1, 0]` as the first element is the X change and the second is the Y. The elements will never overlap.

In the same example if your stack was `[0, -1]` then your screen would look like
```
┌────┐
│   C│
│   B│
│   A│
└────┘
```

### The `func` param
This param is a little interesting, but very important. It specifies exactly where the element should be placed. Here is an example:
```py
lambda size, sizeofobj: (0, round(size[1]/2-sizeofobj[1]/2))
```
What the above's doing is for the Y it's taking the middle point of the screen `(size[1]/2)` and taking away half the height of the object `-sizeofobj[1]/2` which makes the object exactly centered on the screen, with an X position of 0. So, the Center Left of the screen.

Another example is a very simple one:
```py
lambda size, sizeofobj: (0, 0)
```
This is a very simple, it ignores the first 2 params and just positions the element Top Left of the screen.

#### Another way to do it
Another way to do this is by taking a previously existing function and using it. You can find the function at `GO.P___.func` (e.g. `GO.PCBOTTOM.func`)

E.g. if you wanted a center of the screen position but stack it to the right, you can for your function put in `GO.PCCENTER.func`

### WARNING
This can interfere with other pre-existing positions.

Let's say you have made a new position which is the center position but stacking to the left.
```py
GO.PNEW((-1, 0), GO.PCCENTER.func)
```
So if you made 2 elements it would look like this:
```
┌───┐
│   │
│BA │
│   │
└───┘
```
But if you add a third element C to it at `PCCENTER` it **WILL NOT STACK**, it will overlap.
**BE CAREFUL OF THAT**
