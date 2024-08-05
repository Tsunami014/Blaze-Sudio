from enum import Enum
from typing import Any, Union, Iterable
from BlazeSudio.utils.collisions import Shape

Number = Union[int, float]

class BasePlayer:
    # STUFF YOU CAN SET
    """The UID of the entity which is the player start"""
    StartUID: int = None

class BaseCollisions:
    # STUFF YOU CAN SET
    def __call__(self, rect: Shape, movement: list[int], typ: str) -> bool:
        return rect.x, rect.y # The new position of the entity

class SceneEvent(Enum):
    INIT = 0
    """At the start, before anything has loaded"""
    
    LOADED = 1
    """At the start of the scene after all the elements have loaded"""
