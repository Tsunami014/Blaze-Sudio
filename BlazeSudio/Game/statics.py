from enum import Enum
from typing import Any, Union, Iterable

Number = Union[int, float]

class BasePlayer:
    # STUFF YOU CAN SET
    """The UID of the entity which is the player start"""
    StartUID: int = None

class SceneEvent(Enum):
    INIT = 0
    """At the start, before anything has loaded"""
    
    LOADED = 1
    """At the start of the scene after all the elements have loaded"""
