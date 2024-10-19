import pygame
from PIL import Image as PILImage

GLOBALSZE = [100, 100]

class Image:
    def __init__(self, data=None):
        if data is None:
            self.data = [[(0, 0, 0)]]
        else:
            self.data = data
    
    @property
    def size(self):
        return GLOBALSZE
    
    def _toBuffer(self):
        data = []
        for i in range(GLOBALSZE[1]):
            for j in range(GLOBALSZE[0]):
                data.extend(self.get(i, j))
        return bytes(data)
    
    def get(self, y, x):
        return self.data[y % len(self.data)][x % len(self.data[0])]

    def to_pygame(self):
        if GLOBALSZE[0] <= 0 or GLOBALSZE[1] <= 0:
            return pygame.Surface((0, 0))
        return pygame.image.frombuffer(
            self._toBuffer(),
            GLOBALSZE,
            'RGB'
        )

    def to_PIL(self):
        return PILImage.frombytes(
            'RGB',
            GLOBALSZE,
            self._toBuffer()
        )

    @staticmethod
    def from_pygame(surf):
        return Image(
            [[surf.get_at((i, j)) for j in range(surf.get_height())] for i in range(surf.get_width())]
        )
    
    @staticmethod
    def from_PIL(img):
        return Image(
            [
                [img.getpixel((i, j)) for i in range(img.width)] for j in range(img.height)
            ]
        )
    
    def __str__(self):
        return '<Image>'
    def __repr__(self): return str(self)
