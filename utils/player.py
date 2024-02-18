import pygame

class Player:
    def __init__(self, sur):
        self.pos = [0, 0]
        self.sur = sur

    def execute(self, win):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.pos[1] += 10
        elif keys[pygame.K_DOWN]:
            self.pos[1] -= 10
        elif keys[pygame.K_RIGHT]:
            self.pos[0] -= 10
        elif keys[pygame.K_LEFT]:
            self.pos[0] += 10
        win.blit(self.sur, self.pos)
        mw, mh = win.get_width()/2, win.get_height()/2
        pygame.draw.rect(win, (0, 0, 0), (mw-20, mh-20, 40, 40), border_radius=2)
