from enum import Enum
from typing import Any, Union, Iterable

Number = Union[int, float]

class BasePlayer:
    # STUFF YOU CAN SET
    """The UID of the entity which is the player start"""
    StartUID: int = None

class BaseCollisions:
    # STUFF YOU CAN SET
    def __call__(self, pos: list[Number], accel: list[Number], entity: str) -> tuple[list[Number], list[Number]]:
        return [pos[0]+accel[0], pos[1]+accel[1]], accel # Your new position and movement

class SceneEvent(Enum):
    INIT = 0
    """At the start, before anything has loaded"""
    
    LOADED = 1
    """At the start of the scene after all the elements have loaded"""
