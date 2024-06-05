import pygame

# def update(self, sur, pause, mousePos, events, G):

# TODO: Make these classes in Graphics.py and graphics.GUI.* more generic and not have many different functions and not need most of below

class Static:
    def __init__(self, sur, pos):
        self.sur = sur
        self.pos = pos
    
    def update(self, sur, *_):
        sur.blit(self.sur, self.pos)

class Sprite:
    RECTS = []
    def __init__(self, sprite):
        self.sprite = sprite
    def update(self, sur, *_):
        self.sprite.update()
        self.RECTS.append(self.sprite.draw(sur))

class Custom:
    def __init__(self, cls, pass_events):
        self.cls = cls
        self.pass_events = pass_events
    
    def update(self, sur, _, __, events, ___):
        if self.pass_events: self.cls.execute(sur, events)
        else: self.cls.execute(sur)

class Button:
    def __init__(self, sur, rect, pos, col, txt, on_hover_enlarge):
        self.sur = sur
        self.rect = rect
        self.pos = pos
        self.col = col
        self.txt = txt
        self.OHE = on_hover_enlarge
    
    def update(self, sur, pause, mousePos, _, G):
        r = self.rect.copy()
        if not pause:
            col = r.collidepoint(mousePos)
            if self.OHE != -1 and col:
                r.x -= self.OHE
                r.y -= self.OHE
                r.width += self.OHE*2
                r.height += self.OHE*2
        else:
            col = False
        if col:
            G.touchingbtns.append((self.col, r, self.sur, self.pos, self))
        else:
            pygame.draw.rect(sur, self.col, r, border_radius=8)
            sur.blit(self.sur, (self.pos[0]+10, self.pos[1]+10))