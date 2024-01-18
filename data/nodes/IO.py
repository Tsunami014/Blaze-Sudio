from linting import *
#======#

@RMInp(['Val'])
def Value(Val): # If you don't provide type annotation it will be considered 'any'
    '''Returns any value you want, useful for testing and stuff'''
    return {'Out': Val}

#======#

def NumInp(Name: str, Default: int):
    return {'Out': Default}

#======#

def TextInp(Name: str, Default: str):
    return {'Out': Default}

#======#

def BoolInp(Name: str, Default: bool):
    return {'Out': Default}

#======#

def AnyInp(Name: str, Default: Any):
    return {'Out': Default}
