# Funcs:

def RMInp(paramnames: list):
    '''Removes the ability to connect a node to the input for the parameters in the list "paramnames"'''
    pass

def KeepName(paramnames: list):
    '''Makes it still show the text even when the params in "paramnames" already have a value in it'''
    pass

def Remove(paramnames: list):
    '''Removes the params from the list "paramnames" from being shown on the node'''
    pass

# INFO:

'''
Use this if you want:
```
if type(A) != type(B): raise TypeError('Mismatching types!!!')
t = type(A)
```
'''

'''
How this works is the dict is the outputs' names to replace by a new value
So in this case the output with the name 'Out' gets shown as A + B instead 
of it's original 'Out' value if this doesn't error and has all things connected
'''
