from enum import Enum
from typing import Any, Union, Iterable

Number = Union[int, float]

class BasePlayer:
    # STUFF YOU CAN SET
    """The UID of the entity which is the player start"""
    StartUID: int = None

class BaseCollisions:
    # STUFF YOU CAN SET
    NUM_DP = 4
    """The number of decimal places to round to, or -1 to not round at all"""
    
    def __call__(self, pos: list[int], typ: str) -> bool:
        return False # Whether it hits something or not (in this case, it doesn't hit anything)
    
    def num_checks(self, pos: int, typ: str) -> int:
        rpos = str(pos if self.NUM_DP == -1 else round(pos, self.NUM_DP))
        return len(rpos[rpos.find('.'):])

class SceneEvent(Enum):
    INIT = 0
    """At the start, before anything has loaded"""
    
    LOADED = 1
    """At the start of the scene after all the elements have loaded"""
