import pygame

class Image:
    def __init__(self, size=(0, 0), data=None):
        self.size = size
        if data is None:
            self.data = [[(0, 0, 0) for _ in range(size[1])] for _ in range(size[0])]
        else:
            self.data = data
    
    def to_pygame(self):
        if self.size[0] <= 0 or self.size[1] <= 0:
            return pygame.Surface((0, 0))
        return pygame.image.frombuffer(
            bytes([i for j in self.data for k in j for i in k]),
            self.size,
            'RGB'
        )
