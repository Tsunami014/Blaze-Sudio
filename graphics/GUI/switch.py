import pygame

class Switch(pygame.sprite.DirtySprite):
    def __init__(self, win, x, y, default=False):
        self.WIN = win
        self.pos = (x, y)
        self.cirpos = [(x+5, y+5), (x+15, y+5)]
        self.state = default
        super().__init__()
        self.rect = pygame.Rect(x, y, 20, 20)
        self.barrect = pygame.Rect(x+5, y, 20, 10)
    def update(self):
        pygame.draw.rect(self.WIN, (125, 125, 125), self.barrect, border_radius=20)
        pygame.draw.circle(self.WIN, ((0, 255, 0) if self.state else (255, 0, 0)), self.cirpos[int(self.state)], 10)

if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode()
    sprites = pygame.sprite.LayeredDirty()
    curpos = (0, 0)
    for _ in range(20):
        s = Switch(win, *curpos)
        sprites.add(s)
        sze = s.rect.size
        curpos = (curpos[0] + sze[0], curpos[1] + sze[1])
    
    run = True
    while run:
        pygame.event.pump()
        win.fill((255, 255, 255))
        sprites.update()
        pygame.display.update()
    