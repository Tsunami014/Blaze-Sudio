import pygame

__all__ = [
    'Image',
    'Theme',
    'GLOBALTHEME'
]

class Image:
    def __init__(self, fname, startx=0, starty=0, width=None, height=None):
        self.fname = fname
        img = pygame.image.load(fname)
        self.sur = img.subsurface((startx, starty, width or img.get_width(), height or img.get_height()))
    
    def get(self):
        return self.sur


# TODO: A func to load image with options for where to repeat if want to enlarge image etc.

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
