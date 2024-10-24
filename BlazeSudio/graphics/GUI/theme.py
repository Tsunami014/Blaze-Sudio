import pygame

__all__ = [
    'Image',
    'Theme',
    'GLOBALTHEME'
]

class Image:
    def __init__(self, fname, startx=0, starty=0, width=None, height=None, scale=(1, 1)):
        self.fname = fname
        self.sur = pygame.image.load(fname)
        self.crop = (startx, starty, width, height)
        self.scale = scale
    
    def get(self):
        constrain = lambda x: max(min(x, self.sur.get_width()-1), 0)
        w, h = constrain(self.crop[2] or self.sur.get_width()), constrain(self.crop[3] or self.sur.get_height())
        return pygame.transform.scale(
            self.sur.subsurface((constrain(self.crop[0]), 
                                 constrain(self.crop[1]), 
                                 w, h
            )), (w*self.scale[0], h*self.scale[1]))

# TODO: Options for where to repeat if want to enlarge image etc.

class Theme:
    """The basic Theme class. To make a theme you need to derive from this class and then set the global theme to that; e.g.
```python
class MyTheme(Theme):
    BUTTON = pygame.image.load('mybuttonpic.png')

GLOBALTHEME.set_theme(MyTheme)
```
In that specific example it will make all the buttons look like that image.

A cool byproduct from this is you can combine themes with class inheritance; e.g.
```python
class Theme1(Theme):
    BUTTON = pygame.image.load('mybuttonpic.png')
    SLIDER = pygame.image.load('mysliderpic.png')
class Theme2(Theme1):
    SLIDER = pygame.image.load('myothersliderpic.png')
    SOMEOTHERUI = pygame.image.load('myotherUIpic.png')

GLOBALTHEME.set_theme(Theme2)
```
In that scenario, `Theme2` now has the button pic from `Theme1`, in addition to overriding the slider and adding an extra UI element on top :)

Class variables you can change:
 - `BUTTON`
"""
    BUTTON = None
    """The picture of the button."""
    FONTS = []

class GLOBALTHEME:
    THEME = Theme()

    @classmethod
    def set_theme(cls, newTheme):
        cls.THEME = newTheme
