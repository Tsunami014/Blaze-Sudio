import pygame

class Scrollable:
    def __init__(self, sur, pos, goalrect):
        self.sur = sur
        self.pos = pos
        self.goalrect = goalrect
        self.scroll = 0
    def update(self, event):
        if event.type == pygame.MOUSEWHEEL:
            y = event.y - 1
            if 0 <= y <= 1: y = 2
            self.scroll += y
    
    def __call__(self, WIN):
        s = pygame.Surface((self.goalrect))
        s.blit(self.sur, (0, self.scroll))
        WIN.blit(s, self.pos)

if __name__ == '__main__':
    pygame.init()
    w = pygame.display.set_mode()
    from tkinter.filedialog import askopenfilename
    S = Scrollable(pygame.image.load(askopenfilename(defaultextension='.png', filetypes=[('.png', '.png'), ('.jpg', '.jpg')])), (0, 0), (100, 100))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            S.update(event)
        w.fill((0, 0, 0))
        S(w)
        pygame.display.update()
