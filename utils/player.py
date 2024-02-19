import pygame

class Player:
    def __init__(self, sur):
        self.pos = [sur.get_width()/2, sur.get_height()/2]
        self.sur = sur

    def execute(self, win):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.pos[1] -= 10
        elif keys[pygame.K_DOWN]:
            self.pos[1] += 10
        elif keys[pygame.K_RIGHT]:
            self.pos[0] += 10
        elif keys[pygame.K_LEFT]:
            self.pos[0] -= 10
        self.pos[0] = max(min(self.pos[0], self.sur.get_width()), 0)
        self.pos[1] = max(min(self.pos[1], self.sur.get_height()), 0)
        mw, mh = win.get_width()/2, win.get_height()/2
        win.blit(self.sur, [-self.pos[0]+mw, -self.pos[1]+mh])
        pygame.draw.rect(win, (0, 0, 0), (mw-20, mh-20, 40, 40), border_radius=2)
