import pygame

class Player:
    def __init__(self, sur):
        self.pos = [0, 0]
        self.sur = sur

    def execute(self, win, events):
        win.blit(self.sur, self.pos)
