from BlazeSudio.elementGen import Image
from BlazeSudio.graphics import options as GO
from typing import Any

types = {
    'int': float,
    'float': float,
    'number': float,
    'colour': tuple,
    'str': str,
    'bool': bool,
    'image': Image,
    'any': Any,
    '': Any
}

strtypes = {
    int: 'number',
    float: 'number',
    tuple: 'colour',
    str: 'str',
    bool: 'bool',
    Image: 'image',
    Any: 'any',
}

defaults = {
    'number': 0,
    'str': '',
    'bool': False,
    'colour': (255, 255, 50),
    'image': Image(),
    'any': ''
}

def convertTo(value, type):
    valTyp = value.__class__
    if type in (float, int, str):
        try:
            return type(value)
        except:
            return type()
    elif type is tuple:
        if valTyp is tuple:
            return value
        elif valTyp in (int, str):
            return tuple([value]*3)
        return defaults['colour']
    elif type is bool:
        return bool(value)
    elif type is Image:
        if valTyp is Image:
            return value
        elif valTyp is tuple:
            return Image([[value]])
        elif valTyp in (int, float):
            return Image([[(value, value, value)]])
        elif valTyp is str:
            return Image.from_pygame(GO.FREGULAR.render(value, GO.CWHITE))
        return Image()
