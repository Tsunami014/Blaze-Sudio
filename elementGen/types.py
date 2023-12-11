types = {
    'int': int,
    'str': str
}

strtypes = {
    int: 'int',
    str: 'str'
}

defaults = {
    'int': 0,
    'str': ''
}

sizing = {
    'int': lambda num, font: (font.size(str(num))[0], font.size(str(num))[1]+10),
    'str': lambda txt, font: (font.size(str(txt))[0], font.size(str(txt))[1]+10)
}
