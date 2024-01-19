from linting import *
#======#

@Remove(['Val'])
def Value(Val): # If you don't provide type annotation it will be considered 'any'
    '''Returns any value you want, useful for testing and stuff'''
    return {'Out': Val}

#======#

@Remove(['out'])
def Output(Out):
    '''The output for this node'''
    return {'out': Out}

#======#

@RMInp(['Name'])
def NumInp(Name: str, Default: int):
    return {'Out': Default}

#======#

@RMInp(['Name'])
def TextInp(Name: str, Default: str):
    return {'Out': Default}

#======#

@RMInp(['Name'])
def BoolInp(Name: str, Default: bool):
    return {'Out': Default}

#======#

@RMInp(['Name'])
def AnyInp(Name: str, Default: Any):
    return {'Out': Default}
