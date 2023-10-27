# TODO: make each file not need to be dependant on python files from above folders
import pygame
from graphics.GUI import Button
pygame.init()

WIN = pygame.display.set_mode()
pygame.display.toggle_fullscreen()
pygame.display.set_caption('AIHub')

WHITE = (255, 255, 255)
GREEN = (10, 255, 50)
RED = (255, 10, 50)
BLUE = (10, 50, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont('', 52)
title = pygame.font.SysFont('Comic Sans MS', 64, True)
codefont = pygame.font.SysFont('Lucida Sans Typewriter', 16)

class TerminalBar:
    def __init__(self, win, font, spacing=5):
        self.win = win
        self.font = font
        self.spacing = spacing
        self.active = -1
        self.txt = ''
    def pressed(self, event):
        if event.key == pygame.K_RETURN:
            pass
        elif event.key == pygame.K_BACKSPACE:
            self.txt = self.txt[:-1]
        else:
            self.txt += event.unicode
    def toggleactive(self, forceactive=None):
        if forceactive != None:
            if forceactive: self.active = 60
            else: self.active = -1
        if self.active == -1: self.active = 60
        else: self.active = -1
    def update(self):
        t = '>/'+self.txt
        if self.active >= 30: t += '_'
        if self.active >= 0:
            self.active -= 1
            if self.active <= 0: self.active = 60
        r = self.font.render(t, 1, WHITE)
        h = r.get_height()+self.spacing*2
        pygame.draw.rect(self.win, BLACK, pygame.Rect(0, self.win.get_height()-h, self.win.get_width(), h))
        self.win.blit(r, (self.spacing, self.win.get_height()-h+self.spacing))
    def collides(self, x, y):
        r = self.font.render('>/', 1, WHITE)
        h = r.get_height()+self.spacing*2
        return pygame.Rect(0, self.win.get_height()-h, self.win.get_width(), h).collidepoint(x, y)

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.TB = TerminalBar(WIN, codefont)
    def welcome(self):
        welcome = title.render('Welcome to AIHub! :)', 2, BLACK)
        btngen = lambda txt, col, txtcol=BLACK: Button(WIN, txt, col, txtcol, font=font, max_width=300)
        btns = [btngen('Start', GREEN), btngen('Tutorial', RED)]
        run = True
        while run:
            WIN.fill(WHITE)
            updates = [btns[i].update(0, 0 + sum([btns[j].nsurface.get_height() + 20 for j in range(i)])) for i in range(len(btns))]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        break
                    elif self.TB.active != -1:
                        self.TB.pressed(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        for i in [btns[j] for j in range(len(btns)) if updates[j]]:
                            print(i)
                        self.TB.toggleactive(not self.TB.collides(*event.pos))
            WIN.blit(welcome, (WIN.get_width()/2-welcome.get_width()/2, WIN.get_height()/2-welcome.get_height()/2))
            self.TB.update()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    g = Game()
    g.welcome()

pygame.quit()
