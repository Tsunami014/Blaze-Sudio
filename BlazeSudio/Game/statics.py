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
    """If you want to change the values, it is recommended to change them in the `__init__` method of the subclass and use `super().__init__(G, entity)`.
    
    Each value is in units per frame unless specified; and with percents, 1 = 100% and 0 = 0%."""
    def __init__(self, G, entity):
        super().__init__(G, entity)
        # Things to change in __init__ and most of the time remain the same:
        self.max_speed = 3
        """Max speed"""
        self.friction = 0.1
        """Friction (applied each frame) (in percent of current speed)"""
        self.not_hold_fric = 0.01
        """ADDED friction to apply when not holding ANY KEY (you can modify this to be only left-right or whatever) (in percent of current speed)"""
        self.not_hold_grav = [0, 0.04]
        """Decrease in gravity to apply when not holding THE UP KEY (in percent of current gravity strength)"""
        
        # Things to change in your code:
        self._velocity = [0, 0]
        """What to change to modify the speed you want the player to be at. **Changing this every frame will virtually counteract the physics changes!**"""
        self.gravity = [0, 0]
        """Units constantly added to velocity each frame"""

        self._velocity = [0, 0]
        """Don't change this directly; use target_velocity instead"""
        self.position = [0, 0]

        self.holding_any = False
        self.holding_jmp = False
    
    def handle_keys(self):
        keys = pygame.key.get_pressed()
        self.holding_any = True

        # Vertical movement
        if keys[pygame.K_UP] ^ keys[pygame.K_DOWN]:
            if keys[pygame.K_UP]:
                self._velocity[1] -= self.max_speed
            elif keys[pygame.K_DOWN]:
                self._velocity[1] += self.max_speed
        else:
            self.holding_any = False

        # Horizontal movement
        if keys[pygame.K_LEFT] ^ keys[pygame.K_RIGHT]:
            if keys[pygame.K_LEFT]:
                self._velocity[0] -= self.max_speed
            elif keys[pygame.K_RIGHT]:
                self._velocity[0] += self.max_speed
        else:
            self.holding_any = False
    
    def apply_physics(self):
        # Cap the target speed to max_speed
        self._velocity = [max(-self.max_speed, min(self._velocity[0], self.max_speed)),
                                max(-self.max_speed, min(self._velocity[1], self.max_speed))]

        # Apply deceleration to target, so over time (if not constantly set) will slow down
        self._velocity = [self._velocity[0] * (1-(self.friction+(self.not_hold_fric if not self.holding_any else 0))),
                                self._velocity[1] * (1-(self.friction+(self.not_hold_fric if not self.holding_any else 0)))]

        # Add gravity
        self._velocity = [
            self._velocity[0]+(self.gravity[0]*(1 if not self.holding_jmp else (1-self.not_hold_grav[0]))),
            self._velocity[1]+(self.gravity[1]*(1 if not self.holding_jmp else (1-self.not_hold_grav[1])))
        ]

        # Cap the speed to max_speed
        self._velocity = [max(-self.max_speed, min(self._velocity[0], self.max_speed)),
                         max(-self.max_speed, min(self._velocity[1], self.max_speed))]

    def __call__(self, evs):
        self.handle_keys()
        self.apply_physics()
        self.position[0] += self._velocity[0]
        self.position[1] += self._velocity[1]
