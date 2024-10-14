from typing import Any

types = {
    'int': float,
    'float': float,
    'number': float,
    'str': str,
    'bool': bool,
    'any': Any,
    '': Any
}

strtypes = {
    int: 'number',
    float: 'number',
    str: 'str',
    bool: 'bool',
    Any: 'any',
}

defaults = {
    'number': 0,
    'str': '',
    'bool': False,
    'any': ''
}

def getType(val):
    val = val.lower()
    if val == 'false' or val == 'true':
        return 'bool'
    try:
        float(val)
        return 'number'
    except ValueError:
        return 'str'
