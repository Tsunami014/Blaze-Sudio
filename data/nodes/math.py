from linting import *
#======#
@Name('Add')
@Docs('attempt to add the numbers as if they are ints, else just perform addition.')
def node(A: Any, B: Any):
    try:
        return {'Out': int(A) + int(B)}
    except: pass
    return {'Out': A + B}
#======#
@Name('Subtract')
def node(A: int, B: int):
    return {'Out': A - B}
#======#
@Name('Multiply')
def node(A: int, B: int):
    return {'Out': A * B}
#======#
@Name('Divide')
def node(A: int, B: int):
    return {'Out': A / B}
