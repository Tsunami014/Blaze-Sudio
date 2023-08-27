try:
    from utils.characters import *
    from utils.storyline import *
except ImportError:
    from characters import *
    from storyline import *

class World:
    def __init__(self):
        self.storyline = Storyline()
