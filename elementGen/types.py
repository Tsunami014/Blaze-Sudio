from typing import Any

types = {
    'int': int,
    'str': str,
    'any': Any
}

strtypes = {
    int: 'int',
    str: 'str',
    Any: 'any'
}

defaults = {
    'int': 0,
    'str': '',
    'any': ''
}

def getType(val):
    try:
        int(val)
        return 'int'
    except: return 'str'

sizing = {
    'int': lambda num, font: (font.size(str(num))[0], font.size(str(num))[1]+10),
    'str': lambda txt, font: (font.size(str(txt))[0], font.size(str(txt))[1]+10),
    'any': lambda _,   font: (font.size(str('None'))[0], font.size(str("None"))[1]+10)
}
