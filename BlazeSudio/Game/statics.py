import pygame
import math
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
    CamBounds = [None, None, None, None]
    CamDist = 1
    CamPos = [0, 0]
    def __init__(self, G, **settings):
        self.Game: Game = G
    
    def tick(self, keys):
        pass

    def render(self):
        pass

    def postProcessGlobal(self, sur):
        """
        Gets passed the entire sur from the render method.
        """
        return sur

    def postProcessScreen(self, sur, diffs):
        """
        Gets passed the sur after `postProcessGlobal` and after cropped. The output of this will be rendered to the screen.
        """
        return sur

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
    """If you want to change the values, it is recommended to change them in the `__init__` method of the subclass and use `super().__init__(G, entity)`.
    
    Each value is in units per second unless specified; and with percents, 1 = 100% and 0 = 0%."""
    def __init__(self, G, entity):
        super().__init__(G, entity)
        # Things to change in __init__ and most of the time remain the same:
        self.max_speed = 1.25
        """Max speed"""
        self.friction = 0.2
        """Friction (in percent of current speed)"""
        self.not_hold_fric = 0.01
        """ADDED friction to apply when not holding ANY KEY (you can modify this to be only left-right or whatever) (in percent of current speed)"""
        
        # Things to change in your code if neeed:
        self.velocity = [0, 0]
        """What to change to modify the speed you want the player to be at. **Changing this every frame will virtually counteract the physics changes!**"""
        self.gravity = [0, 0]
        """Units constantly added to velocity each frame"""

        self.position = [0, 0]

        self.holding_any = False
    
    def handle_keys(self):
        keys = pygame.key.get_pressed()
        self.holding_any = True

        # Vertical movement
        if keys[pygame.K_UP] ^ keys[pygame.K_DOWN]:
            if keys[pygame.K_UP]:
                self.velocity[1] -= self.max_speed
            elif keys[pygame.K_DOWN]:
                self.velocity[1] += self.max_speed
        else:
            self.holding_any = False

        # Horizontal movement
        if keys[pygame.K_LEFT] ^ keys[pygame.K_RIGHT]:
            if keys[pygame.K_LEFT]:
                self.velocity[0] -= self.max_speed
            elif keys[pygame.K_RIGHT]:
                self.velocity[0] += self.max_speed
        else:
            self.holding_any = False
    
    def apply_physics(self):
        # Cap the target speed to max_speed
        self.velocity = [max(-self.max_speed, min(self.velocity[0], self.max_speed)),
                         max(-self.max_speed, min(self.velocity[1], self.max_speed))]
        
        dt = self.Game.deltaTime

        # Add friction
        fric = 1 - ((self.friction + (self.not_hold_fric if not self.holding_any else 0)) * dt)
        self.velocity = [self.velocity[0]*fric, 
                            self.velocity[1]*fric]
        
        # Apply gravity
        self.velocity = [self.velocity[0] + self.gravity[0] * dt,
                         self.velocity[1] + self.gravity[1] * dt]

        # Cap the speed to max_speed again after applying physics
        self.velocity = [max(-self.max_speed, min(self.velocity[0], self.max_speed)),
                         max(-self.max_speed, min(self.velocity[1], self.max_speed))]

    def __call__(self, evs):
        self.handle_keys()
        self.apply_physics()
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

class AdvBaseEntity(BaseEntity):
    """A slightly more advanced version of BaseEntity.
    
    If you want to change the values, it is recommended to change them in the `__init__` method of the subclass and use `super().__init__(G, entity)`.
    
    Each value is in units per second unless specified; and with percents, 1 = 100% and 0 = 0%."""
    def __init__(self, G, entity):
        super().__init__(G, entity)
        self.max_grav_speed = 1
        """Max speed the gravity can get you"""
        self.grav_fric = 0.2
        """Friction applied in gravity direction (in percent of current gravity strength)"""
        self.friction = 0.2
        """Friction perpendicular to gravity direction (or if no gravity) (in percent of current speed)"""
        self.not_hold_grav = [0, 0.04]
        """Decrease in gravity to apply when not holding THE UP KEY (in percent of current gravity strength)"""
        
        self.holding_jmp = False
    
    def apply_physics(self):
        # Cap the target speed to max_speed
        self.velocity = [max(-self.max_speed, min(self.velocity[0], self.max_speed)),
                         max(-self.max_speed, min(self.velocity[1], self.max_speed))]
        
        dt = self.Game.deltaTime

        # Calculating friction
        fric = 1 - ((self.friction + (self.not_hold_fric if not self.holding_any else 0)) * dt)

        # Project velocity onto gravity direction
        g_mag = math.hypot(*self.gravity)
        if g_mag != 0:
            gdir = (self.gravity[0]/g_mag, self.gravity[1]/g_mag)
            vdot = self.velocity[0]*gdir[0] + self.velocity[1]*gdir[1]
            vdot_fric = max(0, vdot - (self.grav_fric + (self.not_hold_fric if not self.holding_any else 0))*g_mag*dt)
            parallel = (vdot_fric*gdir[0], vdot_fric*gdir[1])
            perpendicular = ((self.velocity[0]-parallel[0])*fric, 
                             (self.velocity[1]-parallel[1])*fric)

            self.velocity = [parallel[0]+perpendicular[0],
                             parallel[1]+perpendicular[1]]
        else:
            self.velocity = [self.velocity[0]*fric, 
                             self.velocity[1]*fric]
        
        # Apply gravity if under max grav speed
        def sign(x):
            return 1 if x > 0 else -1 if x < 0 else 0
        
        if sign(self.velocity[0]) != sign(self.gravity[0]) or abs(self.velocity[0]) < self.max_grav_speed:
            self.velocity[0] += self.gravity[0] * (1 if not self.holding_jmp else (1-self.not_hold_grav[0])) * dt
        if sign(self.velocity[1]) != sign(self.gravity[1]) or abs(self.velocity[1]) < self.max_grav_speed:
            self.velocity[1] += self.gravity[1] * (1 if not self.holding_jmp else (1-self.not_hold_grav[1])) * dt

        # Cap the speed to max_speed again after applying physics
        self.velocity = [max(-self.max_speed, min(self.velocity[0], self.max_speed)),
                         max(-self.max_speed, min(self.velocity[1], self.max_speed))]
