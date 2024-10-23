import pygame
from enum import Enum

__all__ = [
    'MouseState',
    'Mouse'
]

class MouseState(Enum):
    NORMAL = 0
    HOVER = 1
    CLICKING = 2
    TEXT = 3
    GRAB = 4
    WAIT = 5
    NO = 6
    PICK = 7

class BaseMouseUpdater:
    def update(self, state):
        if state == MouseState.NORMAL:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif state == MouseState.HOVER:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif state == MouseState.CLICKING:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif state == MouseState.TEXT:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        elif state == MouseState.GRAB:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
        elif state == MouseState.WAIT:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_WAIT)
        elif state == MouseState.NO:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
        elif state == MouseState.PICK:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        else:
            raise ValueError('Invalid MouseState')

class Mouse:
    STATE = MouseState.NORMAL
    UPDATER = BaseMouseUpdater()

    @classmethod
    def set(cls, state):
        cls.STATE = state
    
    @classmethod
    def set_updater(cls, updater):
        cls.UPDATER = updater
    
    @classmethod
    def update(cls):
        cls.UPDATER.update(cls.STATE)
