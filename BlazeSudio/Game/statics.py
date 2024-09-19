import pygame

class IncorrectLevelError(TypeError):
    """For when the level format is incorrect"""
    pass

# Skeletons: The absolute minimum required things that the class needs
# Bases: Come with some cool functionality

class SkeletonScene:
    useRenderer = True
    def __init__(self, Game, **settings):
        self.Game = Game
        self.CamBounds = [None, None, None, None]
        self.CamDist = 1
    
    @property
    def CamPos(self):
        return [0, 0]
    
    def tick(self, keys):
        pass

    def render(self):
        pass

    def renderUI(self, win, offset, midp, scale):
        pass

class BaseScene(SkeletonScene):
    useRenderer = True
    lvl = 0
    def __init__(self, Game, **settings):
        super().__init__(Game, **settings)
        self.entities = []
        self.CamBounds = [0, 0, *self.currentLvl.sizePx]
    
    @property
    def currentLvl(self):
        return self.Game.world.get_level(self.lvl)
    
    @property
    def CamPos(self):
        return [0, 0]
    
    def tick(self, keys):
        for e in self.entities:
            e(keys)

class SkeletonEntity:
    def __init__(self, Game, entity):
        self.Game = Game
        self.entity = entity
    
    def __call__(self, evs):
        pass

class BaseEntity(SkeletonEntity):
    def __init__(self, Game, entity):
        super().__init__(Game, entity)
        self.pos = [0, 0]
        self.accel = [0, 0]
        self.gravity = [0, 0]
        self.friction = [0.05, 0.05]
        #                   Accel,      decel
        self.accel_amnt = [[0.5, 0.5], [0.25, 0.25]]
        self.max_accel = [2, 2]
    
    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] ^ keys[pygame.K_DOWN]:
            if keys[pygame.K_UP]:
                self.accel[1] -= self.accel_amnt[0][1]
            elif keys[pygame.K_DOWN]:
                self.accel[1] += self.accel_amnt[0][1]
        else:
            if self.accel[1] < -self.accel_amnt[1][1]:
                self.accel[1] += self.accel_amnt[1][1]
            elif self.accel[1] > self.accel_amnt[1][1]:
                self.accel[1] -= self.accel_amnt[1][1]
            else:
                self.accel[1] = 0
        
        if keys[pygame.K_RIGHT] ^ keys[pygame.K_LEFT]:
            if keys[pygame.K_RIGHT]:
                self.accel[0] += self.accel_amnt[0][0]
            elif keys[pygame.K_LEFT]:
                self.accel[0] -= self.accel_amnt[0][0]
        else:
            if self.accel[0] < -self.accel_amnt[1][0]:
                self.accel[0] += self.accel_amnt[1][0]
            elif self.accel[0] > self.accel_amnt[1][0]:
                self.accel[0] -= self.accel_amnt[1][0]
            else:
                self.accel[0] = 0
    
    def handle_accel(self):
        self.accel = [self.accel[0]*(1-self.friction[0]), self.accel[1]*(1-self.friction[1])]
        self.accel = [round(min(max(self.accel[0]+self.gravity[0], -self.max_accel[0]), self.max_accel[0]), 3), round(min(max(self.accel[1]+self.gravity[1], -self.max_accel[1]), self.max_accel[1]), 3)]
    
    def __call__(self, evs):
        self.handle_keys()
        self.handle_accel()
        self.pos = [self.pos[0] + self.accel[0], self.pos[1] + self.accel[1]]
