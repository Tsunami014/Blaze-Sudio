from linting import *
#======#
def Add(A, B):
    '''Attempts to add the numbers as if they are ints, else just perform addition.'''
    try:
        return {'Out': int(A) + int(B)}
    except: pass
    return {'Out': A + B}
#======#
def Subtract(A: int, B: int):
    return {'Out': A - B}
#======#
def Multiply(A: int, B: int):
    return {'Out': A * B}
#======#
def Divide(A: int, B: int):
    return {'Out': A / B}
