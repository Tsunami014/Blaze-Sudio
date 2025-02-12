import pygame
from PIL import Image as PILImage

GLOBALSZE = [100, 100]

class Image:
    def __init__(self, data=None):
        if data is None:
            self.data = []
        else:
            self.data = data
    
    @property
    def size(self):
        return GLOBALSZE
    
    def _toBuffer(self):
        map = self.getMap(0, 0, *GLOBALSZE)
        return bytes([k for i in map for j in i for k in j])
    
    def __getitem__(self, it):
        if not isinstance(it, tuple):
            raise ValueError(
                'Image indices must be a tuple!'
            )
        outit = []
        for i in it:
            if isinstance(it, slice):
                outit.append([i.start, i.stop, i.step])
            elif isinstance(it, int):
                outit.append([i, i])
            else:
                raise ValueError(
                    'Image indices must be slices or ints!'
                )
        if len(it) != 2:
            raise ValueError(
                'Image indices must be 2D!'
            )
        
        if any(len(i) != 2 for i in it):
            li = self.getMap(it[0][0], it[1][0], it[0][1], it[1][1])
            xstep = 1
            ystep = 1
            if it[0][2] is not None:
                xstep = it[0][2]
            if it[1][2] is not None:
                ystep = it[1][2]
            return [
                li[y][::ystep] for y in range(0, len(li), xstep)
            ]
        return self.get(it[0][0], it[1][0])
    
    def getMap(self, x, y, xTo, yTo):
        return [
            [self.get(x2, y2) for x2 in range(x, xTo)] for y2 in range(y, yTo)
        ]

    def get(self, x, y):
        if len(self.data) == 0:
            return (0, 0, 0)
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
