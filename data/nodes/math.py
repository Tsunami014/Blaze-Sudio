# Add any@A any@B | Out #

def node(A, B):
    '''attempt to add the numbers as if they are ints, else just perform addition.'''
    try:
        return {'Out': int(A) + int(B)}
    except: pass
    return {'Out': A + B}

'''
Use this if you want:
```
if type(A) != type(B): raise TypeError('Mismatching types!!!')
t = type(A)
```

How this works is the dict is the outputs' names to replace by a new value
So in this case the output with the name 'Out' gets shown as A + B instead 
of it's original 'Out' value if this doesn't error and has all things connected
'''

# Subtract int@A int@B | Out #

def node(A, B):
    return {'Out': A - B}

# Multiply int@A int@B | Out #

def node(A, B):
    return {'Out': A * B}

# Divide int@A int@B | Out #

def node(A, B):
    return {'Out': A / B}
