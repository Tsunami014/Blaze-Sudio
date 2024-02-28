import pygame

class Switch:
    def __init__(self, win, x, y, size=20, speed=10, default=False):
        self.isswitch = True
        self.WIN = win
        self.pos = (x, y)
        self.size = size
        self.anim = 0
        self.speed = speed
        self.state = default
        self.rect = pygame.Rect(x, y, size, size)
        self.barrect = pygame.Rect(x+size/4, y, size, size/2)
        self.image = pygame.Surface((0, 0))
        self.source_rect = pygame.Rect(0, 0, 0, 0)
    def update(self, *_):
        if self.anim < 0: self.anim = 0
        if self.anim > 15*self.speed: self.anim = 15*self.speed
        if self.anim != (0 if not self.state else 15*self.speed):
            if self.state: self.anim += 1
            else: self.anim -= 1
        pygame.draw.rect(self.WIN, (125, 125, 125), self.barrect, border_radius=self.size)
        pygame.draw.circle(self.WIN, ((0, 255, 0) if self.state else (255, 0, 0)), (self.pos[0]+self.size/4+(self.anim/self.speed)*(self.size/20), self.pos[1]+self.size/4), self.size/2)
    def get(self):
        return self.state
    