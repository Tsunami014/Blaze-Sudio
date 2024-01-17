from linting import *
#======#

@Name('Value')
def node(Value: Any):
    return {'Out': Value}

#======#

@Name('NumInp')
def node(Name: str, Default: int):
    return {'Out': Default}

#======#

@Name('TextInp')
def node(Name: str, Default: str):
    return {'Out': Default}

#======#

@Name('AnyInp')
def node(Name: str, Default: Any):
    return {'Out': Default}
