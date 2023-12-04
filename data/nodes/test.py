# Add int@A int@B | int@Out #

def node(A, B):
    return {'Out': A + B}
'''
How this works is the dict is the outputs' names to replace by a new value
So in this case the output with the name 'Out' gets shown as A + B instead 
of it's original 'Out' value if this doesn't error and has all things connected
'''

# One | int@1 #
def node():
    return {'1': 1}

# Two | int@2 #
def node():
    return {'2': 2}
