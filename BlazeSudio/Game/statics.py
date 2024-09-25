import pygame
# Only import game if is typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from BlazeSudio.Game import Game
from BlazeSudio.ldtk.Pyldtk import Entity

class IncorrectLevelError(TypeError):
    """For when the level format is incorrect"""
    pass

# Skeletons: The absolute minimum required things that the class needs
# Bases: Come with some cool functionality

class SkeletonScene:
    useRenderer = True
    def __init__(self, G, **settings):
        self.Game: Game = G
        self.CamBounds = [None, None, None, None]
        self.CamDist = 1
    
    @property
    def CamPos(self):
        return [0, 0]
    
    def tick(self, keys):
        pass

    def render(self):
        pass

    def renderUI(self, win, scaleFunc):
        pass

class BaseScene(SkeletonScene):
    useRenderer = True
    lvl = 0
    def __init__(self, G, **settings):
        super().__init__(G, **settings)
        self.sur = None
        self.entities = []
        self.CamBounds = [0, 0, *self.currentLvl.sizePx]
    
    @property
    def currentLvl(self):
        return self.Game.world.get_level(self.lvl)
    
    @property
    def CamPos(self):
        return [0, 0]
    
    def renderMap(self):
        self.sur = pygame.Surface(self.currentLvl.sizePx)
        self.sur.fill(self.Game.currentLvL.bgColour)
        self.sur.blit(self.Game.world.get_pygame(self.lvl), (0, 0))
    
    def render(self):
        if self.sur is None:
            self.renderMap()
        return self.sur
    
    def tick(self, keys):
        for e in self.entities:
            e(keys)

class SkeletonEntity:
    def __init__(self, G, entity: Entity):
        self.Game: Game = G
        self.entity: Entity = entity
    
    def __call__(self, evs):
        pass

class BaseEntity(SkeletonEntity):
    def __init__(self, G, entity):
        super().__init__(G, entity)
        self.max_speed = 3  # Maximum speed the entity can reach
        self.acceleration = 0.5  # Rate of acceleration
        self.decell = 0.1 # Rate of decelleration
        self.friction = 0.1  # Friction to slow down the entity
        self.lerp_factor = 0.1  # Factor for smooth interpolation
        
        self.velocity = [0, 0]
        self.target_velocity = [0, 0] # Modify THIS value.
        self.position = [0, 0]
        self.gravity = [0, 0]
    
    @staticmethod
    def lerp(start, end, t):
        """Linearly interpolate between start and end by t."""
        return start + (end - start) * t
    
    def handle_keys(self):
        keys = pygame.key.get_pressed()

        # Vertical movement
        if keys[pygame.K_UP] ^ keys[pygame.K_DOWN]:
            if keys[pygame.K_UP]:
                self.target_velocity[1] -= self.acceleration
            elif keys[pygame.K_DOWN]:
                self.target_velocity[1] += self.acceleration

        # Horizontal movement
        if keys[pygame.K_LEFT] ^ keys[pygame.K_RIGHT]:
            if keys[pygame.K_LEFT]:
                self.target_velocity[0] -= self.acceleration
            elif keys[pygame.K_RIGHT]:
                self.target_velocity[0] += self.acceleration
    
    def apply_physics(self):
        # Cap the speed to max_speed
        self.target_velocity = [max(-self.max_speed, min(self.target_velocity[0], self.max_speed)),
                                max(-self.max_speed, min(self.target_velocity[1], self.max_speed))]
        
        self.target_velocity = [self.target_velocity[0] * (1-self.decell),
                                self.target_velocity[1] * (1-self.decell)]
        
        # Interpolate towards the target velocity for smooth acceleration and deceleration
        self.velocity[0] = self.lerp(self.velocity[0], self.target_velocity[0], self.lerp_factor)
        self.velocity[1] = self.lerp(self.velocity[1], self.target_velocity[1], self.lerp_factor)

        # Add gravity
        self.velocity = [
            self.velocity[0]+self.gravity[0],
            self.velocity[1]+self.gravity[1]
        ]

        # Apply friction to gradually slow down when not accelerating
        if self.target_velocity[0] == 0:
            self.velocity[0] *= (1 - self.friction)
        if self.target_velocity[1] == 0:
            self.velocity[1] *= (1 - self.friction)
        
        # Cap the speed to max_speed
        self.velocity = [max(-self.max_speed, min(self.velocity[0], self.max_speed)),
                         max(-self.max_speed, min(self.velocity[1], self.max_speed))]

    def __call__(self, evs):
        self.handle_keys()
        self.apply_physics()
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]