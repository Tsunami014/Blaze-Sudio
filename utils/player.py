import pygame

class Player:
    def __init__(self, sur):
        self.pos = [sur.get_width()/2, sur.get_height()/2]
        self.sur = sur

    def execute(self, win):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] ^ keys[pygame.K_DOWN]:
            if keys[pygame.K_UP]:
                self.pos[1] -= 10
            elif keys[pygame.K_DOWN]:
                self.pos[1] += 10
        if keys[pygame.K_RIGHT] ^ keys[pygame.K_LEFT]:
            if keys[pygame.K_RIGHT]:
                self.pos[0] += 10
            elif keys[pygame.K_LEFT]:
                self.pos[0] -= 10
        self.pos[0] = max(min(self.pos[0], self.sur.get_width()), 0)
        self.pos[1] = max(min(self.pos[1], self.sur.get_height()), 0)
        mw, mh = win.get_width()/2, win.get_height()/2
        ZC = lambda x: (0 if x < 0 else x) # Zero Check
        diff = ((ZC(mw-self.pos[0]) or -ZC(self.pos[0]-(self.sur.get_width()-mw))),
                (ZC(mh-self.pos[1]) or -ZC(self.pos[1]-(self.sur.get_height()-mh))))
        win.blit(self.sur, [
            -self.pos[0]+mw-diff[0],
            -self.pos[1]+mh-diff[1]
            ])
        pygame.draw.rect(win, (0, 0, 0), (mw-20-diff[0], mh-20-diff[1], 40, 40), border_radius=2)
