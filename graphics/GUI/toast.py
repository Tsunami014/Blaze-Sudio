from math import sqrt

class Toast:
    def __init__(self, surf, pos, bottompos, timeout):
        rnd = lambda inp: [round(inp[0]), round(inp[1])]
        self.surf = surf
        self.pos = rnd(bottompos)
        self.end = rnd(bottompos)
        self.goto = rnd(pos)
        self.initdist = 255 / self.dist()
        self.timeout = timeout
        self.time = 0
        self.living = True
    
    def dist(self):
        return sqrt((self.goto[0] - self.pos[0])**2 + (self.goto[1] - self.pos[1])**2)
    
    def update(self, WIN):
        self.time += 1
        ns = self.surf
        if self.goto != self.pos:
            if self.living: ns.set_alpha(255-self.initdist*self.dist())
            else: ns.set_alpha(self.initdist*self.dist())
            if self.goto[0] != self.pos[0]:
                if self.pos[0] > self.goto[0]: self.pos[0] -= 1
                else: self.pos[0] += 1
            if self.goto[1] != self.pos[1]:
                if self.pos[1] > self.goto[1]: self.pos[1] -= 1
                else: self.pos[1] += 1
        else:
            if not self.living:
                return False
        if self.time > self.timeout and self.living:
            self.pos = self.goto
            self.goto = self.end
            self.living = False
        WIN.blit(ns, self.pos)
        return True
