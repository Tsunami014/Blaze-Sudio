import pygame

class Switch(pygame.sprite.DirtySprite):
    def __init__(self, win, x, y, size=20, speed=10, default=False):
        self.isswitch = True
        self.WIN = win
        self.pos = (x, y)
        self.size = size
        self.anim = 0
        self.speed = speed
        self.state = default
        super().__init__()
        self.rect = pygame.Rect(x, y, size, size)
        self.barrect = pygame.Rect(x+size/4, y, size, size/2)
        self.image = pygame.Surface((0, 0))
        self.source_rect = pygame.Rect(0, 0, 0, 0)
    def update(self):
        if self.anim < 0: self.anim = 0
        if self.anim > 15*self.speed: self.anim = 15*self.speed
        if self.anim != (0 if not self.state else 15*self.speed):
            if self.state: self.anim += 1
            else: self.anim -= 1
        pygame.draw.rect(self.WIN, (125, 125, 125), self.barrect, border_radius=self.size)
        pygame.draw.circle(self.WIN, ((0, 255, 0) if self.state else (255, 0, 0)), (self.pos[0]+self.size/4+(self.anim/self.speed)*(self.size/20), self.pos[1]+self.size/4), self.size/2)
    def get(self):
        return self.state

if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode()
    sprites = pygame.sprite.LayeredDirty()
    curpos = (10, 10)
    for _ in range(19):
        s = Switch(win, *curpos, size=10+2*_)
        sprites.add(s)
        sze = s.rect.size
        curpos = (curpos[0] + sze[0] + 10, curpos[1] + sze[1] + 10)
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    for i in sprites:
                        if i.rect.collidepoint(*pygame.mouse.get_pos()):
                            i.state = not i.state
        win.fill((255, 255, 255))
        sprites.update()
        pygame.display.update()
    pygame.quit()
    