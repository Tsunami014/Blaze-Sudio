from typing import Any

types = {
    'int': float,
    'float': float,
    'number': float,
    'colour': tuple,
    'str': str,
    'bool': bool,
    'any': Any,
    '': Any
}

strtypes = {
    int: 'number',
    float: 'number',
    tuple: 'colour',
    str: 'str',
    bool: 'bool',
    Any: 'any',
}

defaults = {
    'number': 0,
    'str': '',
    'bool': False,
    'colour': (255, 255, 50),
    'any': ''
}
