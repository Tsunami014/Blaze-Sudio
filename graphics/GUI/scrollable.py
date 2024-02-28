import pygame

class Scrollable:
    def __init__(self, sur, pos, goalrect, bounds=(0, float('inf')), outline=10, bar=True, outlinecol=(155, 155, 155)):
        self.sur = sur
        self.bar = bar
        self.pos = pos
        self.goalrect = goalrect
        self.scroll = 0
        self.bounds = bounds
        self.outline = (outline, outlinecol)
    def event_handle(self, event):
        y = event.y - 1
        if 0 <= y <= 1: y = 2
        self.scroll += y * 2
        self.scroll = -min(max(self.bounds[0], -self.scroll), self.bounds[1])
    
    def __call__(self, WIN):
        s = pygame.Surface(self.goalrect)
        s.blit(self.sur, (0, self.scroll))
        WIN.blit(s, self.pos)
