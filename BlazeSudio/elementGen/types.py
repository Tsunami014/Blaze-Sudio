from typing import Any
from inspect import _empty

types = {
    'int': int,
    'str': str,
    'bool': bool,
    'any': Any
}

strtypes = {
    int: 'int',
    str: 'str',
    bool: 'bool',
    Any: 'any',
    _empty: 'any'
}

defaults = {
    'int': 0,
    'str': '',
    'bool': False,
    'any': ''
}

def getType(val):
    if val == 'False' or val == 'True':
        return 'bool'
    try:
        int(val)
        return 'int'
    except: return 'str'

sizing = {
    'int': lambda num, font: (font.winSze(str(num))[0], font.winSze(str(num))[1]+10),
    'str': lambda txt, font: (font.winSze(str(txt))[0], font.winSze(str(txt))[1]+10),
    'bool': lambda _,  __:   (20, 20),
    'any': lambda _,   font: (font.winSze(str('None'))[0], font.winSze(str("None"))[1]+10)
}
